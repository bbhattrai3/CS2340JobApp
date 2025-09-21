from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import JobSeekerProfile

def index(request):
    if request.user.is_authenticated and hasattr(request.user, 'jobseekerprofile'):
        user = request.user
        template_data = {}
        template_data['profile'] = user.jobseekerprofile
        return render(request, 'profiles/my_profile.html', {
                        'template_data': template_data
        })
            
    else:
        return(redirect("profile.create_profile"))

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
        return redirect('profile.index')


        




            