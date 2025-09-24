from django.urls import path
from . import views

app_name = "seeker"

urlpatterns = [
    path("<str:username>/", views.profile_detail, name="profile_detail"),
    path("<str:username>/edit/", views.profile_edit, name="profile_edit"),
    path("<str:username>/edit/privacy", views.profile_edit_privacy, name="profile_edit_privacy"),
]
