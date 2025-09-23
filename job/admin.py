from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "recruiter", "created_at")
    search_fields = ("title", "description", "location")
    list_filter = ("location", "created_at")
    ordering = ("-created_at",)
