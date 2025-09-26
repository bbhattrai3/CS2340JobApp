from django.shortcuts import render

def index(request):
    if not request.user.is_authenticated:
        return render(request, "home/home_page.html", {"active_nav": "home"})
    if hasattr(request.user, "role") and request.user.role == "seeker":
        # Show job search for seekers
        from job.forms import JobSearchForm
        from job.models import Job
        form = JobSearchForm()
        jobs = Job.objects.all()
        return render(request, "job/job_search.html", {"form": form, "jobs": jobs, "active_nav": "jobs"})
    if hasattr(request.user, "role") and request.user.role == "recruiter":
        # Show browse candidates for recruiters with search functionality
        from seeker.models import JobSeekerProfile
        
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
        
        context = {
            'candidates': candidates,
            'search_performed': bool(skills_query or location_query or projects_query),
            'active_nav': 'candidates'
        }
        return render(request, "recruiter/browse_candidates.html", context)
    return render(request, "home/home_page.html", {"active_nav": "home"})