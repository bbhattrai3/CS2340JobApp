from django.shortcuts import render, redirect
from django.contrib.auth import *;
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        return render(request, "home/index.html")
    else:
        return render(request, "home/index.html")

@login_required
def switch_roles(request):
    user = request.user
    if (user.active_role == "seeker"):
        user.active_role = "recruiter"
    elif(user.active_role == "recruiter"):
        user.active_role = "seeker"
    user.save()
    return redirect("home.index")