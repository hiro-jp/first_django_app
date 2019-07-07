from django.db.models.functions import datetime
from django.test import TestCase, Client


# Create your tests here.
from django.urls import reverse
from django.utils import timezone

from users.models import User


def create_logged_in_client(
        client: Client,
        username="testuser",
        password="password",
        employee_code="9999999",
        email="testuser@example.com"
):
    user = User.objects.create_user(
        employee_code=employee_code,
        email=email,
        username=username,
        password=password,
    )
    user.save()
    return client.login(employee_code=employee_code, password=password)


class LoginTest(TestCase):
    def test_can_login(self):
        is_logged_in = create_logged_in_client(self.client)
        self.assertTrue(is_logged_in)

    def test_view_index_with_login_user(self):
        create_logged_in_client(self.client)
        response = self.client.get(reverse('ps_core:index'), follow=True)
        self.assertContains(response, "Home | Profile Sheet")


class UserModelTest(TestCase):
    def test_function_get_yoe(self):
        user = User.objects.create_user(
            employee_code="9999999",
            date_joined=datetime.datetime(2013, 4, 1, 12, 00, 00, 000000, tzinfo=timezone.utc),
        )
        d = timezone.now() - user.date_joined
        yoe = int(d.days / 365)
        self.assertEqual(user.get_yoe(), yoe)
