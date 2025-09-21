from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="profile.index"),
    path('create_profile/', views.create_profile, name = 'profile.create_profile'),
]