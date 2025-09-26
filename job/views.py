from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Job
from .forms import JobForm, JobSearchForm

@login_required
def search_jobs(request):
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

@role_required("recruiter")
def job_list(request):
    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, "job/job_list.html", {"jobs": jobs, "active_nav": "jobs"})

@role_required("recruiter")
def job_post(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            return redirect("job:job_list")
    else:
        form = JobForm()
    return render(request, "job/job_post.html", {"form": form, "active_nav": "jobs"})

@role_required("recruiter")
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect("job:job_list")
    else:
        form = JobForm(instance=job)
    return render(request, "job/job_edit.html", {"form": form, "job": job, "active_nav": "jobs"})

@role_required("recruiter")
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    if request.method == "POST":
        job.delete()
        return redirect("job:job_list")
    return render(request, "job/job_confirm_delete.html", {"job": job, "active_nav": "jobs"})