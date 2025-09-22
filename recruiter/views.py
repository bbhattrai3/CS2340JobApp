# recruiter/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required

recruiter_required = role_required("recruiter")

@login_required
@recruiter_required
def post_job(request):
    return render(request, "recruiter/post_job.html")
