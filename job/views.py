from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Job, Application
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

@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    # Handle duplicates
    if Application.objects.filter(job=job, applicant=request.user).exists():
        return redirect("seeker:applications_list", pk=request.user.id)
    
    if request.method == "POST":
        note = request.POST.get("note", "").strip()
        
        Application.objects.create(
            job=job,
            applicant=request.user,
            note=note
        )

        return redirect("seeker:applications_list", pk=request.user.id)

    return render(request, "job/apply_page.html", {"job":job})

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


@role_required("recruiter")
def job_applicants(request, pk):
    """
    Show all applicants who applied to a given job (only visible to the job's recruiter).
    """
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    stage_data = []
    for stage_value, stage_name in Application.STAGE_CHOICES:
        applications = (
            Application.objects
            .filter(job=job, stage=stage_value)
            .select_related("applicant")
            .order_by("-created_at")
        )
        stage_data.append({
            'stage_value': stage_value,
            'stage_name': stage_name,
            'applications': applications,
            'count': applications.count()
        })

    return render(
        request,
        "job/job_applicants.html",
        {
            "job": job, 
            "stage_data": stage_data, 
            "active_nav": "jobs",
            "total_applicants": sum(stage['count'] for stage in stage_data),
            "STAGE_CHOICES": Application.STAGE_CHOICES
        },
    )

@role_required("recruiter")
@require_POST
def update_application_stage(request, pk):
    """
    Update application stage via AJAX (drag & drop in Kanban).
    """
    try:
        # Get the job first to verify ownership
        job = get_object_or_404(Job, pk=pk, recruiter=request.user)
        
        # Get application ID and new stage from POST data
        application_id = request.POST.get('application_id')
        new_stage = request.POST.get('stage')
        
        print(f"Updating application {application_id} to stage {new_stage} for job {pk}")
        
        if not application_id:
            return JsonResponse({'error': 'Application ID is required'}, status=400)
        
        application = get_object_or_404(Application, pk=application_id, job=job)
        
        # Validate stage choice
        valid_stages = [choice[0] for choice in Application.STAGE_CHOICES]
        if new_stage not in valid_stages:
            return JsonResponse({'error': 'Invalid stage'}, status=400)
        
        # Update application stage
        old_stage = application.stage
        application.stage = new_stage
        application.save()
        
        print(f"Successfully updated application {application_id} from {old_stage} to {new_stage}")
        
        return JsonResponse({
            'success': True,
            'new_stage_name': dict(Application.STAGE_CHOICES)[new_stage]
        })

    except Exception as e:
        print(f"Error updating application stage: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)