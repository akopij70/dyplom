from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from .models import Movie, Vote


class TestViews(TestCase):
    def setUp(self):
        self.testing_movie = Movie.objects.create(title='title', director='director')
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

    def test_all_movies(self):
        response_unauthorized = self.unauthorized_user.get(reverse('movie:get_all_movies'))
        self.assertEquals(response_unauthorized.status_code, 200)

        self.client.login(username='normaluser', password='password123',)
        response_authorized = self.client.get(reverse('movie:get_all_movies'))
        self.assertEquals(response_authorized.status_code, 200)

        self.client.login(username='staffuser', password='password123',)
        response_staff = self.client.get(reverse('movie:get_all_movies'))
        self.assertEquals(response_staff.status_code, 200)

    def test_create(self):
        response_unauthorized = self.unauthorized_user.get(reverse('movie:new_movie'))

        self.assertEquals(response_unauthorized.status_code, 302)

        self.client.login(username='normaluser', password='password123', )
        response_authorized = self.client.get(reverse('movie:new_movie'))
        self.assertEquals(response_authorized.status_code, 302)
        self.client.logout()

        self.client.login(username='staffuser', password='password123', )
        response_staff = self.client.get(reverse('movie:new_movie'))
        self.assertEquals(response_staff.status_code, 200)

    def test_edit(self):
        response_unauthorized = self.unauthorized_user.get(reverse('movie:edit_movie',
                                                                   kwargs={'pk': self.testing_movie.pk}))

        self.assertEquals(response_unauthorized.status_code, 302)

        self.client.login(username='normaluser', password='password123', )
        response_authorized = self.client.get(reverse('movie:edit_movie',
                                                      kwargs={'pk': self.testing_movie.pk}))
        self.assertEquals(response_authorized.status_code, 302)
        self.client.logout()

        self.client.login(username='staffuser', password='password123', )
        response_staff = self.client.get(reverse('movie:edit_movie',
                                                 kwargs={'pk': self.testing_movie.pk}))
        self.assertEquals(response_staff.status_code, 200)

    def test_delete(self):
        response_unauthorized = self.unauthorized_user.get(reverse('movie:delete_movie',
                                                                   kwargs={'pk': self.testing_movie.pk}))

        self.assertEquals(response_unauthorized.status_code, 302)

        self.client.login(username='normaluser', password='password123', )
        response_authorized = self.client.get(reverse('movie:delete_movie',
                                                      kwargs={'pk': self.testing_movie.pk}))
        self.assertEquals(response_authorized.status_code, 302)
        self.client.logout()

        self.client.login(username='staffuser', password='password123', )
        response_staff = self.client.get(reverse('movie:delete_movie',
                                                 kwargs={'pk': self.testing_movie.pk}))
        self.assertEquals(response_staff.status_code, 200)


class VoteTestViews(TestCase):
    def setUp(self):
        self.unauthorized_user = Client()

        self.normaluser1 = User.objects.create_user(
            username='normaluser1',
            password='password123',
        )

        self.normaluser2 = User.objects.create_user(
            username='normaluser2',
            password='password123',
        )

        self.testing_movie = Movie.objects.create(title='title', director='director')
        self.testing_user1_vote = Vote.objects.create(rating=5, user=self.normaluser1, movie=self.testing_movie)

    def test_change_vote(self):
        response_unauthorized = self.unauthorized_user.get(reverse('movie:edit_vote',
                                                                   kwargs={'pk': self.testing_user1_vote.pk}))
        self.assertEquals(response_unauthorized.status_code, 302)

        self.client.login(username='normaluser1', password='password123', )
        response_authorized = self.client.get(reverse('movie:edit_vote',
                                                      kwargs={'pk': self.testing_user1_vote.pk}))
        self.assertEquals(response_authorized.status_code, 200)
        self.client.logout()

        self.client.login(username='normaluser2', password='password123', )
        response_staff = self.client.get(reverse('movie:edit_vote',
                                                 kwargs={'pk': self.testing_user1_vote.pk}))
        self.assertEquals(response_staff.status_code, 404)

