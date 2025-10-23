from django.db import models
from django.conf import settings
from django.utils import timezone

class SavedSearch(models.Model):
    """Model to store recruiter's saved search criteria"""
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField(max_length=255, help_text="Name for this saved search")
    skills_query = models.CharField(max_length=500, blank=True, null=True)
    location_query = models.CharField(max_length=500, blank=True, null=True)
    projects_query = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_notified = models.DateTimeField(null=True, blank=True, help_text="Last time recruiter was notified about new matches")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.recruiter.username}"
    
    def get_search_url(self):
        """Generate URL with search parameters"""
        params = []
        if self.skills_query:
            params.append(f"skills={self.skills_query}")
        if self.location_query:
            params.append(f"location={self.location_query}")
        if self.projects_query:
            params.append(f"projects={self.projects_query}")
        
        query_string = "&".join(params)
        return f"/recruiter/browse-candidates/?{query_string}" if query_string else "/recruiter/browse-candidates/"
    
    def get_matching_candidates(self):
        """Get candidates that match this search criteria"""
        from seeker.models import JobSeekerProfile
        
        candidates = JobSeekerProfile.objects.filter(user__is_staff=False)
        
        if self.skills_query:
            candidates = candidates.filter(skills__icontains=self.skills_query)
        
        if self.location_query:
            candidates = candidates.filter(location__icontains=self.location_query)
        
        if self.projects_query:
            candidates = candidates.filter(projects__icontains=self.projects_query)
        
        return candidates.order_by('-id')
    
    def get_new_matches_since_last_notification(self):
        """Get new candidates that match this search since last notification"""
        candidates = self.get_matching_candidates()
        
        if self.last_notified:
            # Filter candidates created after last notification
            candidates = candidates.filter(user__date_joined__gt=self.last_notified)
        
        return candidates
