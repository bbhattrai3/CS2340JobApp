from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import JobSeekerProfile

def index(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            profile = user.jobseekerprofile
        except:
            return(redirect("/profile/create_profile"))
        return(render(request,'profiles/my_profile.html'))
            

    else:
        return(redirect("accounts.login"))

@login_required
def create_profile(request):

    if hasattr(request.user, 'jobseekerprofile'):
        return redirect('profile.index')

    if request.method == 'GET':
         return render(request, 'profiles/create_profile.html')
        
    elif request.method == 'POST':
        jobSeekerProfile = JobSeekerProfile()
        jobSeekerProfile.user = request.user
        jobSeekerProfile.headline = request.POST['headline']
        jobSeekerProfile.education = request.POST['education']
        jobSeekerProfile.work_experience = request.POST['work_experience']
        jobSeekerProfile.skills = request.POST['skills']
        jobSeekerProfile.links = request.POST['links']
        jobSeekerProfile.save()
        return redirect('')




            