from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.db.models import Count, Q
from .models import User
from .admin_views import UserChangeList, admin_index_view


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    # Enhanced list display with more user information
    list_display = (
        'username', 'email', 'full_name', 'role',
        'is_staff', 'is_active', 'account_age', 'last_activity_days', 'user_actions'
    )

    # Enhanced filters for better user management
    list_filter = ('role', 'is_staff', 'is_active', 'is_superuser', 'date_joined')

    # Search functionality
    search_fields = ('username', 'first_name', 'last_name', 'email')

    # Ordering
    ordering = ('-date_joined',)

    # Enhanced fieldsets for better organization
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'bio')}),
        ('Profile Picture', {'fields': ('profile_picture',), 'classes': ('collapse',)}),
        ('Role & Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': 'Manage user roles and permissions. Staff users can access admin panel.'
        }),
        ('Account Status', {'fields': ('last_login', 'date_joined')}),
        ('Administrative Notes', {'fields': ('admin_notes',), 'classes': ('collapse',)}),
    )

    # Enhanced add fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'password1', 'password2'),
        }),
    )

    # Read-only fields
    readonly_fields = ('date_joined', 'last_login')

    # Actions for bulk operations
    actions = [
        'make_active', 'make_inactive', 'make_staff', 'remove_staff', 
        'assign_recruiter_role', 'assign_seeker_role'
    ]

    def user_actions(self, obj):
        """Add custom action buttons for each user"""
        if obj.pk:
            return format_html(
                '<a class="button" href="{}">View Profile</a> ',
                reverse('admin:accounts_user_change', args=[obj.pk])
            )
        return '-'
    user_actions.short_description = 'Actions'

    def account_age(self, obj):
        """Display account age in days"""
        days = obj.get_account_age_days()
        if days == 0:
            return "Today"
        elif days == 1:
            return "1 day"
        else:
            return f"{days} days"
    account_age.short_description = 'Account Age'

    def last_activity_days(self, obj):
        """Display days since last activity"""
        days = obj.get_last_activity_days()
        if days == 0:
            return format_html('<span style="color: green;">Today</span>')
        elif days <= 7:
            return format_html('<span style="color: orange;">{} days ago</span>', days)
        else:
            return format_html('<span style="color: red;">{} days ago</span>', days)
    last_activity_days.short_description = 'Last Activity'

    def make_active(self, request, queryset):
        """Bulk action to activate users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users were successfully activated.')
    make_active.short_description = "Activate selected users"

    def make_inactive(self, request, queryset):
        """Bulk action to deactivate users"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users were successfully deactivated.')
    make_inactive.short_description = "Deactivate selected users"

    def make_staff(self, request, queryset):
        """Bulk action to make users staff"""
        updated = queryset.update(is_staff=True)
        self.message_user(request, f'{updated} users were successfully made staff.')
    make_staff.short_description = "Make selected users staff"

    def remove_staff(self, request, queryset):
        """Bulk action to remove staff status"""
        updated = queryset.update(is_staff=False)
        self.message_user(request, f'{updated} users were successfully removed from staff.')
    remove_staff.short_description = "Remove staff status from selected users"

    def assign_recruiter_role(self, request, queryset):
        """Bulk action to assign recruiter role"""
        updated = queryset.update(role='recruiter')
        self.message_user(request, f'{updated} users were successfully assigned recruiter role.')
    assign_recruiter_role.short_description = "Assign recruiter role to selected users"

    def assign_seeker_role(self, request, queryset):
        """Bulk action to assign seeker role"""
        updated = queryset.update(role='seeker')
        self.message_user(request, f'{updated} users were successfully assigned seeker role.')
    assign_seeker_role.short_description = "Assign seeker role to selected users"

    def get_queryset(self, request):
        """Optimize queryset for better performance"""
        return super().get_queryset(request).select_related()
    
    def get_changelist(self, request, **kwargs):
        """Use custom ChangeList for user statistics"""
        return UserChangeList


# Customize the admin site
admin.site.site_header = "Job App Administration"
admin.site.site_title = "Job App Admin"
admin.site.index_title = "Welcome to Job App Administration"

# Unregister the default Group admin to customize it
admin.site.unregister(Group)

@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    """Enhanced Group admin for better role management"""
    list_display = ('name', 'user_count')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)

    def user_count(self, obj):
        """Show number of users in each group"""
        return obj.user_set.count()
    user_count.short_description = 'Number of Users'
