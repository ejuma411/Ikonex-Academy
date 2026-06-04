from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class StaffLoginTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="STAFF001",
            password="secret12345",
            is_staff=True,
        )

    def test_anonymous_users_are_redirected_to_login(self):
        response = self.client.get(reverse("dashboard"), secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_staff_no_login_works(self):
        response = self.client.post(
            reverse("login"),
            {"staff_no": "STAFF001", "password": "secret12345"},
            secure=True,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("dashboard"))

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {"staff_no": "STAFF001", "password": "wrong-password"},
            secure=True,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid staff number or password.")
