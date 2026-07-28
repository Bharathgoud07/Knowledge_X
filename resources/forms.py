# resources/forms.py
from django import forms
from .models import (
    Resource,
    SEMESTER_CHOICES,
    RESOURCE_TYPE_CHOICES,
    VERIFICATION_STATUS_CHOICES,
    Comment,
    Rating,
    Subject,
    Report,
)

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


class ResourceForm(forms.ModelForm):
    new_subject_name = forms.CharField(
        required=False,
        max_length=150,
        help_text="If your subject is not in the list, enter it here.",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "E.g. C# Programming"}),
    )

    class Meta:
        model = Resource
        fields = ["title", "description", "subject", "semester", "resource_type", "file"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Resource title"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Describe this resource..."}
            ),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "semester": forms.Select(
                attrs={"class": "form-select"},
                choices=[("", "Select semester")] + list(SEMESTER_CHOICES),
            ),
            "resource_type": forms.Select(
                attrs={"class": "form-select"},
                choices=RESOURCE_TYPE_CHOICES,
            ),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order subjects alphabetically
        qs = Subject.objects.order_by("name")
        self.fields["subject"].queryset = qs

        # Custom label: "Operating System (OS) — CSE" so users can find by abbreviation
        def label_for_subject(obj):
            label = obj.name
            if obj.abbreviation:
                label += f" ({obj.abbreviation})"
            if obj.branch:
                label += f" — {obj.branch}"
            return label

        self.fields["subject"].label_from_instance = label_for_subject

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get("subject")
        new_subject_name = cleaned_data.get("new_subject_name")

        if not subject and not new_subject_name:
            self.add_error("subject", "Please select an existing subject or enter a new one.")
            self.add_error("new_subject_name", "Please select an existing subject or enter a new one.")

        return cleaned_data

    def clean_file(self):
        """Validate file size (max 10MB)."""
        uploaded = self.cleaned_data.get("file")
        if uploaded:
            if uploaded.size > MAX_FILE_SIZE_BYTES:
                raise forms.ValidationError(
                    f"File too large. Maximum allowed size is {MAX_FILE_SIZE_MB}MB. "
                    f"Your file is {uploaded.size / (1024*1024):.1f}MB."
                )
        return uploaded


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "branch", "abbreviation"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject name (e.g. DBMS)"}),
            "branch": forms.TextInput(attrs={"class": "form-control", "placeholder": "Branch (e.g. CSE)"}),
            "abbreviation": forms.TextInput(attrs={"class": "form-control", "placeholder": "Abbreviation (e.g. DBMS)"}),
        }


class AdminResourceForm(forms.ModelForm):
    new_subject_name = forms.CharField(
        required=False,
        max_length=150,
        help_text="If your subject is not in the list, enter it here.",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "E.g. C# Programming"}),
    )

    class Meta:
        model = Resource
        fields = [
            "title",
            "description",
            "subject",
            "semester",
            "resource_type",
            "file",
            "is_public",
            "verification_status",
            "verification_note",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Resource title"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Describe this resource..."}
            ),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "semester": forms.Select(
                attrs={"class": "form-select"},
                choices=[("", "Select semester")] + list(SEMESTER_CHOICES),
            ),
            "resource_type": forms.Select(
                attrs={"class": "form-select"},
                choices=RESOURCE_TYPE_CHOICES,
            ),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "verification_status": forms.Select(
                attrs={"class": "form-select"},
                choices=VERIFICATION_STATUS_CHOICES,
            ),
            "verification_note": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Optional verification note"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = Subject.objects.order_by("name")
        self.fields["subject"].queryset = qs
        def label_for_subject(obj):
            label = obj.name
            if obj.abbreviation:
                label += f" ({obj.abbreviation})"
            if obj.branch:
                label += f" — {obj.branch}"
            return label
        self.fields["subject"].label_from_instance = label_for_subject

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get("subject")
        new_subject_name = cleaned_data.get("new_subject_name")
        if not subject and not new_subject_name:
            self.add_error("subject", "Please select an existing subject or enter a new one.")
            self.add_error("new_subject_name", "Please select an existing subject or enter a new one.")
        return cleaned_data

    def clean_file(self):
        uploaded = self.cleaned_data.get("file")
        if uploaded:
            if uploaded.size > MAX_FILE_SIZE_BYTES:
                raise forms.ValidationError(
                    f"File too large. Maximum allowed size is {MAX_FILE_SIZE_MB}MB. "
                    f"Your file is {uploaded.size / (1024*1024):.1f}MB."
                )
        return uploaded


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["reason"]
        widgets = {
            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Explain what is wrong with this material...",
                }
            )
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Write your comment...",
                }
            )
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["stars"]
        widgets = {
            "stars": forms.Select(
                attrs={"class": "form-select"},
                choices=[
                    (i, f"{i} Star" if i == 1 else f"{i} Stars") for i in range(1, 6)
                ],
            )
        }
