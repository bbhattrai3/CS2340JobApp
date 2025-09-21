from django.shortcuts import render
from django.contrib.auth import *;

def index(request):
    if request.user.is_authenticated:
        user = request.user
        template_data = {}
        template_data['status'] = user.active_role
        return render(request, "home/index.html",
                  {'template_data': template_data})
    else:
        return render(request, "home/index.html")