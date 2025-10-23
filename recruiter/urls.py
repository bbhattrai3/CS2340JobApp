# recruiter/urls.py
from django.urls import path
from . import views

app_name = "recruiter"

urlpatterns = [
    path("post-job/", views.post_job, name="post_job"),
    path("browse-candidates/", views.browse_candidates, name="browse_candidates"),
    path("candidate/<str:username>/contact/", views.contact_candidate, name="contact_candidate"),
    path("save-search/", views.save_search, name="save_search"),
    path("saved-searches/", views.saved_searches, name="saved_searches"),
    path("saved-searches/<int:search_id>/delete/", views.delete_saved_search, name="delete_saved_search"),
]
