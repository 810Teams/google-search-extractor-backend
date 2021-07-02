"""
    User Application Django Admin
    user/admin.py
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    """ User admin """
    list_display = ('id', 'username', 'name', 'is_active', 'is_staff', 'is_superuser')
    readonly_fields = ('last_login', 'created_at', 'updated_at')
    list_per_page = 20

    fieldsets = (
        (None, {'fields': ('username', 'name', 'password')}),
        ('Timestamps', {'fields': ('last_login', 'created_at', 'updated_at')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

admin.site.register(get_user_model(), UserAdmin)
