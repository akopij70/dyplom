from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.unauthorized_user = Client()

        self.authorized_user = User.objects.create_user(
            username='normaluser',
            password='password123',
        )

        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='password123',
            is_staff=True,
        )

    def test_index_page(self):
        response_unauthorized = self.unauthorized_user.get(reverse('core:index'))
        self.assertEquals(response_unauthorized.status_code, 200)

        self.client.login(username='normaluser', password='password123', )
        response_authorized = self.client.get(reverse('core:index'))
        self.assertEquals(response_authorized.status_code, 200)
        self.client.logout()

        self.client.login(username='staffuser', password='password123', )
        response_staff = self.client.get(reverse('core:index'))
        self.assertEquals(response_staff.status_code, 200)

    def test_contact_page(self):
        response_unauthorized = self.unauthorized_user.get(reverse('core:contact'))
        self.assertEquals(response_unauthorized.status_code, 200)

        self.client.login(username='normaluser', password='password123', )
        response_authorized = self.client.get(reverse('core:contact'))
        self.assertEquals(response_authorized.status_code, 200)
        self.client.logout()

        self.client.login(username='staffuser', password='password123', )
        response_staff = self.client.get(reverse('core:contact'))
        self.assertEquals(response_staff.status_code, 200)
