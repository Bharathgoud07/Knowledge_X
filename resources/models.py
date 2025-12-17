# resources/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator

# --------- Choices ---------
SEMESTER_CHOICES = [
    (1, "1st Semester"),
    (2, "2nd Semester"),
    (3, "3rd Semester"),
    (4, "4th Semester"),
    (5, "5th Semester"),
    (6, "6th Semester"),
    (7, "7th Semester"),
    (8, "8th Semester"),
]

RESOURCE_TYPE_CHOICES = [
    ("NOTES", "Notes"),
    ("HANDWRITTEN", "Handwritten Notes"),
    ("IMP_QUESTIONS", "Important Questions"),
    ("DIAGRAM", "Diagrams / Charts"),
    ("REFERENCE", "Reference Material"),
]

VERIFICATION_STATUS_CHOICES = [
    ("PENDING", "Pending"),
    ("APPROVED", "Approved"),
    ("REJECTED", "Rejected"),
]


# -------------------------
# SUBJECT MODEL
# -------------------------
class Subject(models.Model):
    name = models.CharField(max_length=150)
    branch = models.CharField(
        max_length=50,
        blank=True,  # e.g. "CSE", "ECE"
    )

    def __str__(self):
        return f"{self.name} ({self.branch})" if self.branch else self.name


# -------------------------
# RESOURCE MODEL
# -------------------------
class Resource(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resources",
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resources",
    )

    semester = models.PositiveSmallIntegerField(
        choices=SEMESTER_CHOICES,
        blank=True,
        null=True,
    )
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPE_CHOICES,
        default="NOTES",
    )

    file = models.FileField(
        upload_to="uploads/resources/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "jpg",
                    "jpeg",
                    "png",
                    "docx",
                    "zip",
                    "ppt",
                    "pptx",
                ]
            )
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # Analytics
    download_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)

    # Public link
    is_public = models.BooleanField(default=True)

    # Verification
    verification_status = models.CharField(
        max_length=10,
        choices=VERIFICATION_STATUS_CHOICES,
        default="PENDING",
    )
    verified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="verified_resources",
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_note = models.TextField(blank=True)

    # AI Generated Helper Fields
    auto_summary = models.TextField(blank=True)
    auto_questions = models.TextField(
        blank=True,
        help_text="AI-generated Important Questions (one per line).",
    )
    auto_diagram_notes = models.TextField(
        blank=True,
        help_text="AI-generated diagram / explanation notes.",
    )

    def __str__(self):
        return self.title

    # ---- Helpers for file icons ----
    @property
    def file_ext(self):
        name = self.file.name.lower()
        return name.split(".")[-1] if "." in name else ""

    @property
    def is_image(self):
        return self.file_ext in ["jpg", "jpeg", "png"]

    # ---- Ratings helpers ----
    @property
    def rating_count(self):
        return self.ratings.count()

    @property
    def average_rating(self):
        from django.db.models import Avg

        avg = self.ratings.aggregate(avg=Avg("stars"))["avg"]
        return round(avg, 1) if avg else 0

    def is_favorited_by(self, user):
        if not user.is_authenticated:
            return False
        return self.favorites.filter(user=user).exists()

    @property
    def is_verified(self):
        return self.verification_status == "APPROVED"


# -------------------------
# REPORT MODEL
# -------------------------
class Report(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("REVIEWED", "Reviewed"),
        ("RESOLVED", "Resolved"),
    ]

    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="reports",
    )
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reports",
    )
    reason = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="OPEN",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    handled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report #{self.id} - {self.resource.title}"


# -------------------------
# FAVORITE MODEL
# -------------------------
class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "resource")

    def __str__(self):
        return f"{self.user.username} → {self.resource.title}"


# -------------------------
# COMMENTS MODEL
# -------------------------
class Comment(models.Model):
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField()

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"


# -------------------------
# RATING MODEL
# -------------------------
class Rating(models.Model):
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ratings",
    )

    stars = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("resource", "user")

    def __str__(self):
        return f"{self.resource.title}: {self.stars}★"


# -------------------------
# NOTIFICATION MODEL
# -------------------------
class Notification(models.Model):
    NOTIF_TYPE_CHOICES = [
        ("COMMENT", "Comment"),
        ("REPLY", "Reply"),
        ("RATING", "Rating"),
        ("REPORT", "Report"),
        ("REPORT_STATUS", "Report Status Update"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    notif_type = models.CharField(
        max_length=20,
        choices=NOTIF_TYPE_CHOICES,
    )

    message = models.CharField(max_length=255)

    resource = models.ForeignKey(
        Resource,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        "Comment",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    report = models.ForeignKey(
        "Report",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notif → {self.user.username}: {self.message[:30]}"


# -------------------------
# VISIT MODEL
# -------------------------
class Visit(models.Model):
    """
    Stores each page visit.
    Used for admin analytics: daily visits, popular pages, etc.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="visits",
        help_text="Who visited (null if not logged in).",
    )
    path = models.CharField(
        max_length=255,
        help_text="Requested URL path",
    )
    method = models.CharField(
        max_length=6,
        help_text="HTTP method (GET/POST)",
    )
    is_authenticated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["path"]),
        ]

    def __str__(self):
        user_part = self.user.username if self.user else "anonymous"
        return f"{user_part} -> {self.path} @ {self.created_at:%Y-%m-%d %H:%M}"
