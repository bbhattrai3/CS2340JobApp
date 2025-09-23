# recruiter/urls.py
from django.urls import path
from . import views

app_name = "recruiter"

urlpatterns = [
    path("post-job/", views.post_job, name="post_job"),
    path("browse-candidates/", views.browse_candidates, name="browse_candidates"),
    path("candidate/<str:username>/contact/", views.contact_candidate, name="contact_candidate"),
]
