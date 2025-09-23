from django.urls import path
from . import views

app_name = "job"

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("post/", views.job_post, name="job_post"),
    path("<int:pk>/edit/", views.job_edit, name="job_edit"),
    path("<int:pk>/delete/", views.job_delete, name="job_delete"),
]
