from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    release_date = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='movies_thumbnails', blank=True, null=True, default='movies_thumbnails'
                                                                                                '/logo.png')

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Nasze filmy'

    def __str__(self) -> str:
        return f'{self.title} ({self.release_date})'


class Vote(models.Model):
    class PossibleRatings:
        RATES = [(i / 10, str(i / 10)) for i in range(10, 90, 5)]  # ratings 1.0 - 8.5

    movie = models.ForeignKey(Movie, related_name='votes', on_delete=models.CASCADE)
    rating = models.DecimalField(choices=PossibleRatings.RATES, max_digits=3, decimal_places=1)
    comment = models.CharField(max_length=255, blank=True, null=True)
    # comment_about_the_movie = models.Te(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'movie')
        verbose_name_plural = 'Oceny'
