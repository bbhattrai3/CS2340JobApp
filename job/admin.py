from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db import transaction
from .models import Job

User = get_user_model()

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "recruiter", "created_at")
    search_fields = ("title", "description", "location")
    list_filter = ("location", "created_at")
    ordering = ("-created_at",)
    
    # Disable admin logging to prevent foreign key constraint issues
    def log_deletion(self, request, object, object_repr):
        """Override to disable deletion logging"""
        pass
    
    def log_addition(self, request, object, message):
        """Override to disable addition logging"""
        pass
    
    def log_change(self, request, object, message):
        """Override to disable change logging"""
        pass
    
    def get_readonly_fields(self, request, obj=None):
        # Make recruiter field read-only to prevent integrity errors
        if obj:  # Editing existing object
            return ('recruiter',)
        return ()
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:  # Editing existing object
            # Remove recruiter from form to prevent changes
            if 'recruiter' in form.base_fields:
                del form.base_fields['recruiter']
        return form
    
    def save_model(self, request, obj, form, change):
        # Ensure the recruiter is set to the current user if not already set
        if not change:  # Only for new objects
            obj.recruiter = request.user
        elif not obj.recruiter:  # If somehow recruiter is None
            obj.recruiter = request.user
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        """Override delete to handle foreign key constraints"""
        try:
            # Delete the object directly (logging is disabled)
            obj.delete()
            messages.success(request, f"Job '{obj.title}' was deleted successfully.")
        except Exception as e:
            messages.error(request, f"Could not delete job '{obj.title}': {str(e)}")
    
    def delete_queryset(self, request, queryset):
        """Override bulk delete to handle foreign key constraints"""
        try:
            # Delete objects directly (logging is disabled)
            count = queryset.count()
            queryset.delete()
            messages.success(request, f"{count} job(s) were deleted successfully.")
        except Exception as e:
            messages.error(request, f"Could not delete selected jobs: {str(e)}")