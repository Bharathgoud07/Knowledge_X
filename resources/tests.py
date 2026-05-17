from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Subject, Resource, Favorite, Comment, Rating, Notification


class ResourceModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="resourceuser",
            password="password123"
        )
        self.subject = Subject.objects.create(
            name="Computer Networks",
            branch="CSE"
        )

    def test_resource_creation(self):
        """Test creating a resource with a mock file."""
        mock_file = SimpleUploadedFile(
            "test_file.pdf",
            b"Mock file content",
            content_type="application/pdf"
        )

        resource = Resource.objects.create(
            owner=self.user,
            title="Test Notes",
            description="Important test notes",
            subject=self.subject,
            semester=5,
            resource_type="NOTES",
            file=mock_file
        )

        self.assertEqual(resource.title, "Test Notes")
        self.assertEqual(resource.owner.username, "resourceuser")
        self.assertEqual(resource.download_count, 0)
        self.assertEqual(resource.view_count, 0)
        self.assertEqual(resource.verification_status, "PENDING")

    def test_subject_str(self):
        self.assertEqual(str(self.subject), "Computer Networks (CSE)")


class ResourceViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="viewuser", password="pass123"
        )
        self.subject = Subject.objects.create(name="DBMS", branch="CSE")
        self.client.login(username="viewuser", password="pass123")

        mock_file = SimpleUploadedFile(
            "notes.pdf", b"PDF content", content_type="application/pdf"
        )
        self.resource = Resource.objects.create(
            owner=self.user, title="DBMS Notes", subject=self.subject,
            semester=3, resource_type="NOTES", file=mock_file
        )

    def test_resource_list_loads(self):
        response = self.client.get(reverse("resources:resource_list"))
        self.assertEqual(response.status_code, 200)

    def test_resource_detail_loads(self):
        response = self.client.get(
            reverse("resources:resource_detail", args=[self.resource.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_upload_page_loads(self):
        response = self.client.get(reverse("resources:upload_resource"))
        self.assertEqual(response.status_code, 200)


class InteractionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="interact_user", password="pass123"
        )
        self.subject = Subject.objects.create(name="OS", branch="CSE")
        self.client.login(username="interact_user", password="pass123")

        mock_file = SimpleUploadedFile(
            "os.pdf", b"PDF content", content_type="application/pdf"
        )
        self.resource = Resource.objects.create(
            owner=self.user, title="OS Notes", subject=self.subject,
            semester=5, resource_type="NOTES", file=mock_file
        )

    def test_toggle_favorite(self):
        url = reverse("resources:resource_toggle_favorite", args=[self.resource.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Favorite.objects.filter(user=self.user, resource=self.resource).exists())

    def test_add_comment(self):
        url = reverse("resources:resource_detail", args=[self.resource.pk])
        response = self.client.post(url, {
            "comment_submit": "1",
            "text": "Great notes!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(user=self.user, text="Great notes!").exists())

    def test_add_rating(self):
        url = reverse("resources:resource_detail", args=[self.resource.pk])
        response = self.client.post(url, {
            "rating_submit": "1",
            "stars": 4,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Rating.objects.filter(user=self.user, resource=self.resource, stars=4).exists())

    def test_notification_creation_on_comment(self):
        """Test that a notification is NOT created when owner comments on own resource."""
        url = reverse("resources:resource_detail", args=[self.resource.pk])
        self.client.post(url, {"comment_submit": "1", "text": "Self comment"})
        # Owner commenting on their own resource should not create a notification
        self.assertEqual(Notification.objects.filter(user=self.user).count(), 0)

    def test_notifications_page_loads(self):
        response = self.client.get(reverse("resources:notifications_list"))
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_page_loads(self):
        response = self.client.get(reverse("resources:leaderboard"))
        self.assertEqual(response.status_code, 200)
