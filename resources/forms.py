# resources/forms.py
from django import forms
from .models import (
    Resource,
    SEMESTER_CHOICES,
    RESOURCE_TYPE_CHOICES,
    Comment,
    Rating,
    Subject,
    Report,
)


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["title", "description", "subject", "semester", "resource_type", "file"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
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
        self.fields["subject"].queryset = Subject.objects.order_by("name")


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
