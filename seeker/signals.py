from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from .models import JobSeekerProfile
from messaging.models import Message

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_jobseeker_profile(sender, instance, created, **kwargs):
    if created and instance.role == "seeker":
        JobSeekerProfile.objects.create(user=instance)

@receiver(post_save, sender=JobSeekerProfile)
def notify_recruiters_profile_update(sender, instance, created, **kwargs):
    """Notify recruiters when a job seeker profile is created or updated and matches saved searches"""
    from recruiter.models import SavedSearch
    
    # Get all saved searches
    saved_searches = SavedSearch.objects.all()
    
    for saved_search in saved_searches:
        # Check if this profile matches the search criteria
        matches = False
        
        # Check skills match
        if saved_search.skills_query and instance.skills:
            skills_query_lower = saved_search.skills_query.lower()
            skills_lower = instance.skills.lower()
            if skills_query_lower in skills_lower:
                matches = True
        
        # Check location match
        if saved_search.location_query and instance.location:
            location_query_lower = saved_search.location_query.lower()
            location_lower = instance.location.lower()
            if location_query_lower in location_lower:
                matches = True
        
        # Check projects match
        if saved_search.projects_query and instance.projects:
            projects_query_lower = saved_search.projects_query.lower()
            projects_lower = instance.projects.lower()
            if projects_query_lower in projects_lower:
                matches = True
        
        if matches:
            # Check if we've already notified about this profile for this search recently
            # (within the last hour to avoid spam)
            from django.utils import timezone
            from datetime import timedelta
            
            recent_cutoff = timezone.now() - timedelta(hours=1)
            
            # Check if there's a recent notification for this profile and search
            recent_notification = Message.objects.filter(
                sender__username='system',
                recipient=saved_search.recruiter,
                thread_id=f"search_notification_{saved_search.id}",
                created_at__gte=recent_cutoff,
                content__icontains=instance.user.username
            ).exists()
            
            if not recent_notification:
                # Determine if this is a new profile or updated profile
                profile_status = "new candidate" if created else "updated candidate"
                action_verb = "joined" if created else "updated their profile"
                
                # Create notification message
                subject = f"New Candidate Match for '{saved_search.name}'"
                
                # Build message content
                message_content = f"Hello {saved_search.recruiter.first_name or saved_search.recruiter.username},\n\n"
                message_content += f"A {profile_status} has {action_verb} and matches your saved search '{saved_search.name}'.\n\n"
                
                message_content += "Candidate Details:\n"
                message_content += f"• Name: {instance.user.first_name or instance.user.username}"
                if instance.user.last_name:
                    message_content += f" {instance.user.last_name}"
                message_content += f" (@{instance.user.username})\n"
                
                if instance.headline and instance.privacy.get('headline') == 'public':
                    message_content += f"• Headline: {instance.headline}\n"
                
                if instance.skills and instance.privacy.get('skills') == 'public':
                    skills_preview = instance.skills[:200] + "..." if len(instance.skills) > 200 else instance.skills
                    message_content += f"• Skills: {skills_preview}\n"
                
                if instance.location and instance.privacy.get('location') == 'public':
                    message_content += f"• Location: {instance.location}\n"
                
                if instance.education and instance.privacy.get('education') == 'public':
                    education_preview = instance.education[:100] + "..." if len(instance.education) > 100 else instance.education
                    message_content += f"• Education: {education_preview}\n"
                
                message_content += f"\nView full profile: https://genewc.pythonanywhere.com/seeker/profile/{instance.user.username}/\n"
                message_content += f"Run saved search: https://genewc.pythonanywhere.com{saved_search.get_search_url()}\n\n"
                message_content += "Best regards,\nJobApp Team"
                
                # Get or create system user for notifications
                from accounts.models import User
                system_user, _ = User.objects.get_or_create(
                    username='system',
                    defaults={
                        'email': 'system@jobapp.com',
                        'first_name': 'System',
                        'last_name': 'User',
                        'role': 'recruiter',
                        'is_staff': True
                    }
                )
                
                # Send internal message
                Message.objects.create(
                    sender=system_user,
                    recipient=saved_search.recruiter,
                    subject=subject,
                    content=message_content,
                    thread_id=f"search_notification_{saved_search.id}"
                )
                
                # Update last notified timestamp
                saved_search.last_notified = timezone.now()
                saved_search.save()