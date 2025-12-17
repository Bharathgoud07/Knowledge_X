# resources/admin.py
from django.contrib import admin
from django.utils import timezone

from .models import (
    Subject,
    Resource,
    Report,
    Favorite,
    Comment,
    Rating,
    Notification,
)

# --------------------------
# SUBJECT ADMIN
# --------------------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# --------------------------
# RESOURCE ADMIN
# --------------------------
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subject",
        "owner",
        "resource_type",
        "semester",
        "verification_status",   # real DB field
        "is_verified",           # @property – OK in list_display
        "download_count",
        "view_count",
        "created_at",
    )

    # ❗ IMPORTANT: use model fields only here (no `is_verified`)
    list_filter = (
        "subject",
        "resource_type",
        "verification_status",
        "semester",
    )

    search_fields = (
        "title",
        "description",
        "owner__username",
        "subject__name",
    )

    readonly_fields = (
        "download_count",
        "view_count",
        "created_at",
        "verified_at",
    )

    fieldsets = (
        ("Basic Info", {
            "fields": ("owner", "title", "description", "file"),
        }),
        ("Academic", {
            "fields": ("subject", "semester", "resource_type"),
        }),
        ("Analytics", {
            "fields": ("download_count", "view_count"),
        }),
        ("Verification", {
            "fields": (
                "verification_status",
                "verified_by",
                "verified_at",
                "verification_note",
            ),
        }),
        ("AI Helper Fields", {
            "fields": ("auto_summary", "auto_questions", "auto_diagram_notes"),
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        When staff/admin changes verification_status,
        automatically fill verified_by + verified_at.
        """
        if change and "verification_status" in form.changed_data:
            obj.verified_by = request.user
            obj.verified_at = timezone.now()
        super().save_model(request, obj, form, change)


# --------------------------
# REPORT ADMIN
# --------------------------
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "resource",
        "reporter",
        "status",
        "created_at",
        "handled_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("resource__title", "reporter__username", "reason")
    readonly_fields = ("created_at", "handled_at")

    def save_model(self, request, obj, form, change):
        """
        When status is changed to RESOLVED or REVIEWED,
        set handled_at time.
        """
        if change and "status" in form.changed_data:
            obj.handled_at = timezone.now()
        super().save_model(request, obj, form, change)


# --------------------------
# FAVORITE ADMIN
# --------------------------
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "resource", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "resource__title")


# --------------------------
# COMMENT ADMIN
# --------------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "resource", "parent", "created_at")
    list_filter = ("created_at",)
    search_fields = (
        "user__username",
        "resource__title",
        "text",
    )


# --------------------------
# RATING ADMIN
# --------------------------
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("resource", "user", "stars", "created_at")
    list_filter = ("stars", "created_at")
    search_fields = ("resource__title", "user__username")


# --------------------------
# NOTIFICATION ADMIN
# --------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "notif_type",
        "message",
        "resource",
        "comment",
        "report",
        "is_read",
        "created_at",
    )
    list_filter = ("notif_type", "is_read", "created_at")
    search_fields = ("user__username", "message")
