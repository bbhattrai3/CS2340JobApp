from django.shortcuts import render


def index(request):
    if not request.user.is_authenticated:
        return render(request, "home/home_page.html", {"active_nav": "home"})

    if getattr(request.user, "role", None) == "seeker":
        from job.forms import JobSearchForm
        from job.models import Job
        from seeker.models import JobSeekerProfile

        form = JobSearchForm(request.GET or None)
        jobs = Job.objects.all()

        if form.is_valid():
            data = form.cleaned_data
            if data.get("title"):
                jobs = jobs.filter(title__icontains=data["title"])
            if data.get("skills"):
                skills_list = [s.strip().lower() for s in data["skills"].split(",") if s.strip()]
                for skill in skills_list:
                    jobs = jobs.filter(skills__icontains=skill)
            if data.get("location"):
                jobs = jobs.filter(location__icontains=data["location"])
            if data.get("salary_min") is not None:
                jobs = jobs.filter(salary_min__gte=data["salary_min"])
            if data.get("salary_max") is not None:
                jobs = jobs.filter(salary_max__lte=data["salary_max"])
            if data.get("remote"):
                jobs = jobs.filter(remote=True)
            if data.get("visa_sponsorship"):
                jobs = jobs.filter(visa_sponsorship=True)

        recommended_jobs = []
        profile = JobSeekerProfile.objects.filter(user=request.user).first()
        if profile and profile.skills:
            seeker_skills = set([
                s.strip().lower() for s in profile.skills.strip().split(",") if s.strip()
            ])
            job_scores = []
            
            for job in Job.objects.all():
                if not job.skills:
                    continue
                job_skills = set([s.strip().lower() for s in job.skills.strip().split(",") if s.strip()])
                overlap = seeker_skills & job_skills
                if overlap:
                    job_scores.append((job, len(overlap)))

            job_scores.sort(key=lambda x: x[1], reverse=True)
            recommended_jobs = [job for job, score in job_scores[:10]]

        return render(request, "job/job_search.html", {"form": form, "jobs": jobs, "recommended_jobs": recommended_jobs, "active_nav": "jobs"})

    if getattr(request.user, "role", None) == "recruiter":
        from seeker.models import JobSeekerProfile
        from job.models import Job
        # Get search parameters from URL
        skills_query = request.GET.get('skills', '').strip()
        location_query = request.GET.get('location', '').strip()
        projects_query = request.GET.get('projects', '').strip()
        
        # Start with all job seeker profiles (exclude admin users)
        candidates = JobSeekerProfile.objects.filter(user__is_staff=False)

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
    }

    return render(request, "recruiter/browse_candidates.html", context)
    return render(request, "home/home_page.html", {"active_nav": "home"})