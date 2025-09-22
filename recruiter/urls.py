# recruiter/urls.py
from django.urls import path
from . import views

app_name = "recruiter"

urlpatterns = [
    path("post-job/", views.post_job, name="post_job"),
]
