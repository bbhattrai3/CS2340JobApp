from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    # Show username, first name, last name, email, role, and staff status in the list
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'is_staff', 'is_active')

    # Optional: add filters
    list_filter = ('role', 'is_staff', 'is_active')

    # Ensure 'role' appears in the edit and add forms
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
