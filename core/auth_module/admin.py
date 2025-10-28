from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "email",
        "is_agent",
        "is_admin_reviewer",
        "is_superuser",
        "is_active",
        "is_suspended"
    ]