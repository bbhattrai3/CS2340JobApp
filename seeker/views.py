from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import JobSeekerProfile
from .forms import JobSeekerProfileForm

@login_required
def profile_edit(request, pk):
    profile = get_object_or_404(JobSeekerProfile, pk=pk, user=request.user)

    if request.method == "POST":
        form = JobSeekerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("seeker:profile_detail", pk=profile.user.id)
    else:
        form = JobSeekerProfileForm(instance=profile)

    return render(request, "seeker/profile_edit.html", {"form": form, "profile": profile})

@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(JobSeekerProfile, user__id=pk)
    return render(request, "seeker/profile_detail.html", {"profile": profile})
