import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from .models import Event


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

    def test_get_events(self):
        unauthorized_response = self.unauthorized_user.get(reverse("event:all_events"))
        self.assertEquals(unauthorized_response.status_code, 200)

    def test_create(self):
        unauthorizedresponse = self.unauthorized_user.get(reverse("event:new_event"))
        self.assertEquals(unauthorizedresponse.status_code, 302)

        self.client.login(username='normaluser', password='password123',)
        authorized_response = self.client.get(reverse("event:new_event"))
        self.assertEquals(authorized_response.status_code, 302)
        self.client.logout()

        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse("event:new_event"))
        self.assertEquals(response.status_code, 200)

    def test_edit(self):
        self.event = Event.objects.create(date=datetime.date.today())
        unauthorizedresponse = self.unauthorized_user.get(reverse("event:edit_event", kwargs={'pk': self.event.pk}))
        self.assertEquals(unauthorizedresponse.status_code, 302)

        self.client.login(username='normaluser', password='password123',)
        authorized_response = self.client.get(reverse("event:edit_event", kwargs={'pk': self.event.pk}))
        self.assertEquals(authorized_response.status_code, 302)
        self.client.logout()

        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse("event:edit_event", kwargs={'pk': self.event.pk}))
        self.assertEquals(response.status_code, 200)


class TestModels(TestCase):
    def setUp(self) -> None:
        self.event = Event.objects.create(date=datetime.date.today())

    def test_creating_current_event(self):
        self.assertTrue(self.event.event_in_current_week())
        self.assertFalse(self.event.event_in_past())
        self.assertFalse(self.event.event_in_future())

    def test_editing_date_year(self):
        current_month = datetime.date.today().month
        current_day = datetime.date.today().day
        past_year = (datetime.date.today().year - 1)

        self.event.date = datetime.date(past_year, current_month, current_day)
        self.assertFalse(self.event.event_in_current_week())
        self.assertTrue(self.event.event_in_past())
        self.assertFalse(self.event.event_in_future())

        future_year = past_year + 2

        self.event.date = datetime.date(future_year, current_month, current_day)
        self.assertFalse(self.event.event_in_current_week())
        self.assertFalse(self.event.event_in_past())
        self.assertTrue(self.event.event_in_future())

    def test_editing_to_future(self):
        self.event.date = datetime.date.today()
        self.event.date = self.event.date + datetime.timedelta(days=7)
        self.assertFalse(self.event.event_in_current_week())
        self.assertFalse(self.event.event_in_past())
        self.assertTrue(self.event.event_in_future())

        self.event.date = self.event.date + datetime.timedelta(days=15)
        self.assertFalse(self.event.event_in_current_week())
        self.assertFalse(self.event.event_in_past())
        self.assertTrue(self.event.event_in_future())

    def test_editing_to_past(self):
        self.event.date = datetime.date.today()
        self.event.date = self.event.date - datetime.timedelta(days=7)
        self.assertFalse(self.event.event_in_current_week())
        self.assertTrue(self.event.event_in_past())
        self.assertFalse(self.event.event_in_future())

        self.event.date = self.event.date - datetime.timedelta(days=15)
        self.assertFalse(self.event.event_in_current_week())
        self.assertTrue(self.event.event_in_past())
        self.assertFalse(self.event.event_in_future())
