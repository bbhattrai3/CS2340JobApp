from django.shortcuts import render

def index(request):
    if not request.user.is_authenticated:
        return render(request, "home/home_page.html", {"active_nav": "home"})
    if hasattr(request.user, "role") and request.user.role == "seeker":
        # Show job search for seekers with filtering
        from job.forms import JobSearchForm
        from job.models import Job
<<<<<<< HEAD
        form = JobSearchForm(request.GET or None)
        jobs = Job.objects.all()
=======
        
        form = JobSearchForm(request.GET or None)
        jobs = Job.objects.all()
        
>>>>>>> 732a9500df4635bb09328f03ea9ecd856083a122
        if form.is_valid():
            data = form.cleaned_data
            if data.get('title'):
                jobs = jobs.filter(title__icontains=data['title'])
            if data.get('skills'):
                skills_list = [s.strip().lower() for s in data['skills'].split(',') if s.strip()]
                for skill in skills_list:
                    jobs = jobs.filter(skills__icontains=skill)
            if data.get('location'):
                jobs = jobs.filter(location__icontains=data['location'])
            if data.get('salary_min') is not None:
                jobs = jobs.filter(salary_min__gte=data['salary_min'])
            if data.get('salary_max') is not None:
                jobs = jobs.filter(salary_max__lte=data['salary_max'])
            if data.get('remote'):
                jobs = jobs.filter(remote=True)
            if data.get('visa_sponsorship'):
                jobs = jobs.filter(visa_sponsorship=True)
<<<<<<< HEAD
=======
        
>>>>>>> 732a9500df4635bb09328f03ea9ecd856083a122
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