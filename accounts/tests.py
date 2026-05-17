from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile


class AccountsModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="test@example.com"
        )

    def test_profile_creation(self):
        """Test that a profile is automatically created when a user is created."""
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user.username, "testuser")

    def test_profile_str(self):
        """Test string representation of the profile."""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), "Profile of testuser")


class AuthViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="loginuser",
            password="testpass123",
            email="login@example.com"
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse("accounts:login"), {
            "identifier": "loginuser",
            "password": "testpass123",
        })
        self.assertEqual(response.status_code, 302)

    def test_login_with_invalid_password(self):
        response = self.client.post(reverse("accounts:login"), {
            "identifier": "loginuser",
            "password": "wrongpassword",
        })
        self.assertEqual(response.status_code, 200)

    def test_register_duplicate_email(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "newuser",
            "email": "login@example.com",
            "password": "strongpass123",
            "confirm_password": "strongpass123",
        })
        # Should stay on register page with error
        self.assertEqual(response.status_code, 200)

    def test_logout_redirect(self):
        self.client.login(username="loginuser", password="testpass123")
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)

    def test_profile_requires_login(self):
        response = self.client.get(reverse("accounts:my_profile"))
        self.assertEqual(response.status_code, 302)

    def test_password_reset_page_loads(self):
        response = self.client.get(reverse("accounts:password_reset"))
        self.assertEqual(response.status_code, 200)
