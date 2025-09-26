# recruiter/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.decorators import role_required
from seeker.models import JobSeekerProfile
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .forms import ContactCandidateForm

recruiter_required = role_required("recruiter")

@login_required
@recruiter_required
def post_job(request):
    return render(request, "recruiter/post_job.html", {"active_nav": "jobs"})

@login_required
@recruiter_required
def browse_candidates(request):
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
        'search_performed': bool(skills_query or location_query or projects_query)
    }
    context["active_nav"] = "candidates"
    return render(request, "recruiter/browse_candidates.html", context)


@login_required
@recruiter_required
def contact_candidate(request, username):
    profile = get_object_or_404(JobSeekerProfile, user__username=username)
    candidate_email = profile.user.email
    if request.method == 'POST':
        form = ContactCandidateForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = request.user.email or None
            try:
                send_mail(subject, message, from_email, [candidate_email])
                messages.success(request, 'Email sent to candidate.')
            except Exception as e:
                messages.error(request, f'Failed to send email: {e}')
            return redirect('recruiter:browse_candidates')
    else:
        form = ContactCandidateForm()

    return render(request, 'recruiter/contact_candidate.html', {'form': form, 'profile': profile})
