import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractUser
)

from datetime import timedelta

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    employee_id = models.CharField(max_length=10, unique=True, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    is_admin_reviewer = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=True)
    is_suspended = models.BooleanField(default=False)
    suspension_reason = models.TextField(blank=True, null=True)
    suspension_time = models.DateTimeField(blank=True, null=True)

    password_last_changed = models.DateTimeField(default=timezone.now)

    failed_login_attempts = models.IntegerField(default=0)
    lockout_until = models.DateTimeField(null=True, blank=True)

    PASSWORD_EXPIRY_DAYS = 90

    def is_password_expired(self):
        return timezone.now() > self.password_last_changed + timedelta(days=self.PASSWORD_EXPIRY_DAYS)

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []  # prompts when creating superuser

    def suspend(self, reason: str = ""):
        self.is_suspended = True
        self.suspension_reason = reason
        self.suspension_time = timezone.now()
        self.save()

    def reactivate(self):
        self.is_suspended = False
        self.suspension_reason = None
        self.suspension_time = None
        self.save()

    def can_login(self):
        if self.is_suspended:
            return False

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_admin_reviewer = True
            self.is_agent = True
        return super().save(*args, **kwargs)