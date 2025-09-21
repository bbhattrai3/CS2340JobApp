from django.contrib import admin
from django.contrib.auth import get_user_model


# Register your models here.
User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'active_role')
    