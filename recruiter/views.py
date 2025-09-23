# recruiter/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.decorators import role_required
from seeker.models import JobSeekerProfile

recruiter_required = role_required("recruiter")

@login_required
@recruiter_required
def post_job(request):
    return render(request, "recruiter/post_job.html")

@login_required
@recruiter_required
def browse_candidates(request):
    # Get search parameters from URL
    skills_query = request.GET.get('skills', '').strip()
    location_query = request.GET.get('location', '').strip()
    projects_query = request.GET.get('projects', '').strip()
    
    # Start with all job seeker profiles
    candidates = JobSeekerProfile.objects.all()
    
    # Apply filters based on search criteria
    if skills_query:
        candidates = candidates.filter(skills__icontains=skills_query)
    
    if location_query:
        candidates = candidates.filter(location__icontains=location_query)
    
    if projects_query:
        candidates = candidates.filter(projects__icontains=projects_query)
    
    # Order by most recent first
    candidates = candidates.order_by('-id')
    
    context = {
        'candidates': candidates,
        'search_performed': bool(skills_query or location_query or projects_query)
    }
    
    return render(request, "recruiter/browse_candidates.html", context)
