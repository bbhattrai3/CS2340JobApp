from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import role_required
from .models import Job
from .forms import JobForm

@role_required("recruiter")
def job_list(request):
    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, "job/job_list.html", {"jobs": jobs})

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
    return render(request, "job/job_post.html", {"form": form})

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
    return render(request, "job/job_edit.html", {"form": form, "job": job})

@role_required("recruiter")
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    if request.method == "POST":
        job.delete()
        return redirect("job:job_list")
    return render(request, "job/job_confirm_delete.html", {"job": job})