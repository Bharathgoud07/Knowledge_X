import socket

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Profile


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "username"})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"})
    )
    password = forms.CharField(
        label="Password",
        min_length=8,
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"})
    )

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        # prevent dummy/fake domains
        blocked = {"example.com", "fake.com", "test.com", "mailinator.com"}
        domain = email.split("@")[-1]

        if domain in blocked:
            raise forms.ValidationError("Please use a real email provider.")

        try:
            socket.getaddrinfo(domain, None)
        except socket.gaierror:
            raise forms.ValidationError("Email domain does not appear to exist. Please enter a valid address.")

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean_password(self):
        """Run Django's built-in password validators (same as password reset)."""
        password = self.cleaned_data.get("password")
        if password:
            # Create a temporary user object for validation context
            username = self.data.get("username", "")
            email = self.data.get("email", "")
            temp_user = User(username=username, email=email)
            try:
                validate_password(password, user=temp_user)
            except ValidationError as e:
                raise forms.ValidationError(list(e.messages))
        return password

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        cpw = cleaned.get("confirm_password")

        if pw and cpw and pw != cpw:
            self.add_error("confirm_password", "Passwords don't match.")
        return cleaned


class EmailLoginForm(forms.Form):
    identifier = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "full_name",
            "college",
            "branch",
            "bio",
            "github",
            "linkedin",
            "website_url",
            "location",
            "picture",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "college": forms.TextInput(attrs={"class": "form-control"}),
            "branch": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "github": forms.URLInput(attrs={"class": "form-control"}),
            "linkedin": forms.URLInput(attrs={"class": "form-control"}),
            "website_url": forms.URLInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }
