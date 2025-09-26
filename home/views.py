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
        # Show browse candidates for recruiters
        from seeker.models import JobSeekerProfile
        candidates = JobSeekerProfile.objects.all().order_by('-id')
        return render(request, "recruiter/browse_candidates.html", {"candidates": candidates, "active_nav": "candidates"})
    return render(request, "home/home_page.html", {"active_nav": "home"})