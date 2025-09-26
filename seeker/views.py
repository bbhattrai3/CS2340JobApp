from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import JobSeekerProfile, Link
from .forms import JobSeekerProfileForm
from django import forms


@login_required
def profile_edit(request, username):
    profile = get_object_or_404(JobSeekerProfile, user__username=username, user=request.user)

    if request.method == "POST":
        form = JobSeekerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            links = request.POST.getlist("links")  
            profile.links.all().delete()
            for url in links:
                if url.strip():
                    Link.objects.create(profile=profile, url=url)

            return redirect("seeker:profile_detail", username=profile.user.username)
    else:
        form = JobSeekerProfileForm(instance=profile)

    return render(request, "seeker/profile_edit.html", {"form": form, "profile": profile})

@login_required
@login_required
def profile_edit_privacy(request, username):
    profile = get_object_or_404(JobSeekerProfile, user__username=username, user=request.user)

    class DynamicPrivacyForm(forms.Form):
        pass
    
    for field_name, setting in profile.privacy.items():
        choices = [
            (JobSeekerProfile.Privacy.PUBLIC, "Public"),
            (JobSeekerProfile.Privacy.PRIVATE, "Private")
        ]
        field = forms.ChoiceField(
            choices=choices, 
            initial=setting, 
            label=field_name.replace("_", " ").title(),
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        DynamicPrivacyForm.base_fields[field_name] = field

    if request.method == "POST":
        form = DynamicPrivacyForm(request.POST)
        if form.is_valid():
            profile.privacy.update(form.cleaned_data)
            profile.save()
            return redirect("seeker:profile_detail", username=profile.user.username)
    else:
        form = DynamicPrivacyForm()

    return render(request, "seeker/profile_edit_privacy.html", {
        "form": form, 
        "profile": profile
    })

@login_required
def profile_detail(request, username):
    # Try to get by username, fallback to user ID
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        profile = get_object_or_404(JobSeekerProfile, user__username=username)
    except:
        try:
            user = get_object_or_404(User, id=username)
            profile = get_object_or_404(JobSeekerProfile, user=user)
        except:
            raise
    visible_fields = {}
    for field, setting in profile.privacy.items():
        if can_view(setting, request.user, profile.user):
            if field == 'links':
                # Handle links specially since it's a related manager
                visible_fields[field] = profile.links.all()
            else:
                visible_fields[field] = getattr(profile, field)
    return render(request, "seeker/profile_detail.html", {"profile": profile, "visible_fields": visible_fields})

def can_view(field_privacy, viewer, owner):
    if field_privacy == "public":
        return True
    if field_privacy == "private" and viewer == owner:
        return True
    return False