from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, LoginOTP

# --------------------------
# PROFILE INLINE FOR USER ADMIN
# --------------------------
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "get_college",
        "get_email_verified",
    )

    def get_college(self, instance):
        return instance.profile.college if hasattr(instance, "profile") else ""
    get_college.short_description = "College"

    def get_email_verified(self, instance):
        return instance.profile.email_verified if hasattr(instance, "profile") else False
    get_email_verified.short_description = "Email Verified"
    get_email_verified.boolean = True

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# --------------------------
# PROFILE ADMIN
# --------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "full_name",
        "college",
        "branch",
        "email_verified",
        "login_streak",
    )
    list_filter = ("email_verified", "branch", "college")
    search_fields = ("user__username", "full_name", "college", "branch")
    readonly_fields = ("login_streak", "longest_streak", "last_login_date", "created_at", "updated_at")

    fieldsets = (
        ("User", {
            "fields": ("user",)
        }),
        ("Basic Info", {
            "fields": ("full_name", "college", "branch", "bio", "location", "picture")
        }),
        ("Social Links", {
            "fields": ("github", "linkedin", "website_url")
        }),
        ("Account Info", {
            "fields": ("email_verified", "email_verified_at")
        }),
        ("Streaks & Dates", {
            "fields": ("login_streak", "longest_streak", "last_login_date", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

# --------------------------
# LOGIN OTP ADMIN
# --------------------------
@admin.register(LoginOTP)
class LoginOTPAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "is_used", "created_at")
    list_filter = ("is_used", "created_at")
    search_fields = ("user__username", "code")
    readonly_fields = ("user", "code", "created_at", "is_used")

    def has_add_permission(self, request):
        return False  # OTPs shouldn't be added manually
