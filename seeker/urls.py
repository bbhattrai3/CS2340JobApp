from django.urls import path
from . import views

app_name = "seeker"

urlpatterns = [
    path("<int:pk>/", views.profile_detail, name="profile_detail"),
    path("<int:pk>/edit/", views.profile_edit, name="profile_edit"),
]
