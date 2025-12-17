from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    # Basic info
    full_name = models.CharField(max_length=150, blank=True)
    college = models.CharField(max_length=150, blank=True)
    branch = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)

    # Social links
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    website_url = models.URLField(blank=True)

    # Location
    location = models.CharField(max_length=150, blank=True)

    # Avatar
    picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    # Login streaks
    login_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_login_date = models.DateField(null=True, blank=True)

    # Email verification
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class LoginOTP(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="login_otps"
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        if self.is_used:
            return False
        return (timezone.now() - self.created_at).total_seconds() <= 600

    def __str__(self):
        return f"OTP for {self.user.username} ({self.code})"
