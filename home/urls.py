from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home.index"),
    path("switch_roles", views.switch_roles, name="home.switch_roles"),
]