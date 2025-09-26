from django.shortcuts import render

def index(request):
    if not request.user.is_authenticated:
        return render(request, "home/home_page.html", {"active_nav": "home"})
    if hasattr(request.user, "role") and request.user.role == "seeker":
        # Show job search for seekers
        from job.forms import JobSearchForm
        from job.models import Job
        form = JobSearchForm(request.GET or None)
        jobs = Job.objects.all()
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
        return render(request, "job/job_search.html", {"form": form, "jobs": jobs, "active_nav": "jobs"})
    if hasattr(request.user, "role") and request.user.role == "recruiter":
        # Show browse candidates for recruiters
        from seeker.models import JobSeekerProfile
        candidates = JobSeekerProfile.objects.all().order_by('-id')
        return render(request, "recruiter/browse_candidates.html", {"candidates": candidates, "active_nav": "candidates"})
    return render(request, "home/home_page.html", {"active_nav": "home"})