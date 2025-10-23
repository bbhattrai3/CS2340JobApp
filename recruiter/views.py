# recruiter/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.decorators import role_required
from accounts.models import User
from job.models import Job
from seeker.models import JobSeekerProfile
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .forms import ContactCandidateForm, SaveSearchForm
from .models import SavedSearch
from messaging.models import Message

recruiter_required = role_required("recruiter")

@login_required
@recruiter_required
def post_job(request):
    return render(request, "recruiter/post_job.html", {"active_nav": "jobs"})

@login_required
@recruiter_required
def browse_candidates(request):
    # Get search parameters from URL
    skills_query = request.GET.get('skills', '').strip()
    location_query = request.GET.get('location', '').strip()
    projects_query = request.GET.get('projects', '').strip()
    
    # Start with all job seeker profiles (exclude admin users)
    candidates = JobSeekerProfile.objects.filter(user__is_staff=False)
    
    # Apply filters based on search criteria
    if skills_query:
        candidates = candidates.filter(skills__icontains=skills_query)
    
    if location_query:
        candidates = candidates.filter(location__icontains=location_query)
    
    if projects_query:
        candidates = candidates.filter(projects__icontains=projects_query)
    
    # Order by most recent first
    candidates = candidates.order_by('-id')
    
    job_skills = set()
    jobs = Job.objects.filter(recruiter=request.user)
    
    for job in jobs:
        if job.skills:
            job_skills.update([s.strip().lower() for s in job.skills.strip().split(",") if s.strip()])

    recommended_scores = []
    for candidate in JobSeekerProfile.objects.filter(user__is_staff=False):
        if candidate.skills:
            candidate_skills = set([s.strip().lower() for s in candidate.skills.strip().split(",") if s.strip()])
            overlap = candidate_skills & job_skills
            if len(overlap) >= 1:
                recommended_scores.append((candidate, len(overlap)))
    
    recommended_scores.sort(key=lambda x: x[1], reverse=True)
    recommended_candidates = [candidate for candidate, score in recommended_scores[:10]]
    print("Recommended:", [c.user.username for c in recommended_candidates])
    
    context = {
        'candidates': candidates,
        'recommended_candidates': recommended_candidates,
        'search_performed': bool(skills_query or location_query or projects_query),
        'active_nav': 'candidates',
    # Get saved searches for this recruiter
    saved_searches = SavedSearch.objects.filter(recruiter=request.user)
    
    context = {
        'candidates': candidates,
        'search_performed': bool(skills_query or location_query or projects_query),
        'saved_searches': saved_searches,
        'current_search': {
            'skills': skills_query,
            'location': location_query,
            'projects': projects_query,
        }
    }

    return render(request, "recruiter/browse_candidates.html", context)


@login_required
@recruiter_required
def contact_candidate(request, username):
    profile = get_object_or_404(JobSeekerProfile, user__username=username)
    candidate_email = profile.user.email
    if request.method == 'POST':
        form = ContactCandidateForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = request.user.email or None
            try:
                send_mail(subject, message, from_email, [candidate_email])
                messages.success(request, 'Email sent to candidate.')
            except Exception as e:
                messages.error(request, f'Failed to send email: {e}')
            return redirect('recruiter:browse_candidates')
    else:
        form = ContactCandidateForm()

    return render(request, 'recruiter/contact_candidate.html', {'form': form, 'profile': profile})
    return render(request, 'recruiter/contact_candidate.html', {'form': form, 'profile': profile})

@login_required
@recruiter_required
@require_POST
def save_search(request):
    """Save current search criteria"""
    skills_query = request.POST.get('skills', '').strip()
    location_query = request.POST.get('location', '').strip()
    projects_query = request.POST.get('projects', '').strip()
    search_name = request.POST.get('name', '').strip()
    
    if not search_name:
        messages.error(request, 'Please provide a name for your search.')
        return redirect('recruiter:browse_candidates')
    
    # Check if a search with the same criteria already exists
    existing_search = SavedSearch.objects.filter(
        recruiter=request.user,
        skills_query=skills_query,
        location_query=location_query,
        projects_query=projects_query
    ).first()
    
    if existing_search:
        messages.info(request, f'A search with these criteria already exists: "{existing_search.name}"')
        return redirect('recruiter:browse_candidates')
    
    # Create new saved search
    saved_search = SavedSearch.objects.create(
        recruiter=request.user,
        name=search_name,
        skills_query=skills_query,
        location_query=location_query,
        projects_query=projects_query
    )
    
    messages.success(request, f'Search "{search_name}" saved successfully!')
    return redirect('recruiter:browse_candidates')

@login_required
@recruiter_required
def saved_searches(request):
    """View to manage saved searches"""
    saved_searches = SavedSearch.objects.filter(recruiter=request.user)
    return render(request, 'recruiter/saved_searches.html', {
        'saved_searches': saved_searches,
        'active_nav': 'candidates'
    })

@login_required
@recruiter_required
def delete_saved_search(request, search_id):
    """Delete a saved search"""
    saved_search = get_object_or_404(SavedSearch, id=search_id, recruiter=request.user)
    search_name = saved_search.name
    saved_search.delete()
    messages.success(request, f'Search "{search_name}" deleted successfully!')
    return redirect('recruiter:saved_searches')

def notify_recruiters_of_new_matches():
    """Function to notify recruiters about new matches for their saved searches"""
    from seeker.models import JobSeekerProfile
    
    # Get all saved searches
    saved_searches = SavedSearch.objects.all()
    
    for saved_search in saved_searches:
        # Get new matches since last notification
        new_matches = saved_search.get_new_matches_since_last_notification()
        
        if new_matches.exists():
            # Create notification message
            match_count = new_matches.count()
            subject = f"New Candidate Matches for '{saved_search.name}'"
            
            # Build message content
            message_content = f"Hello {saved_search.recruiter.first_name or saved_search.recruiter.username},\n\n"
            message_content += f"We found {match_count} new candidate{'s' if match_count > 1 else ''} that match your saved search '{saved_search.name}'.\n\n"
            message_content += "Search Criteria:\n"
            if saved_search.skills_query:
                message_content += f"• Skills: {saved_search.skills_query}\n"
            if saved_search.location_query:
                message_content += f"• Location: {saved_search.location_query}\n"
            if saved_search.projects_query:
                message_content += f"• Projects: {saved_search.projects_query}\n"
            
            message_content += f"\nNew Matches:\n"
            for profile in new_matches[:5]:  # Show first 5 matches
                message_content += f"• {profile.user.first_name or profile.user.username} "
                if profile.user.last_name:
                    message_content += f"{profile.user.last_name} "
                message_content += f"(@{profile.user.username})\n"
                if profile.headline and profile.privacy.get('headline') == 'public':
                    message_content += f"  - {profile.headline}\n"
                if profile.skills and profile.privacy.get('skills') == 'public':
                    skills_preview = profile.skills[:100] + "..." if len(profile.skills) > 100 else profile.skills
                    message_content += f"  - Skills: {skills_preview}\n"
                message_content += "\n"
            
            if match_count > 5:
                message_content += f"... and {match_count - 5} more matches.\n\n"
            
            message_content += f"\nView all matches: https://genewc.pythonanywhere.com{saved_search.get_search_url()}\n\n"
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
