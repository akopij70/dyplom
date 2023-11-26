from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


class Movie(models.Model):
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    director = models.CharField(max_length=255, blank=False, null=False)
    release_date = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='movies_thumbnails', blank=True, null=True, default='movies_thumbnails'
                                                                                                '/logo.png')

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Nasze filmy'

    def calculate_average_rating(self):
        new_average = Vote.objects.filter(movie__title=self.title).aggregate(Avg('rating'))['rating__avg']
        self.average_rating = new_average
        self.save()

    def __str__(self) -> str:
        return f'{self.title} ({self.release_date})'


class Vote(models.Model):
    class PossibleRatings:
        RATES = [(i / 10, str(i / 10)) for i in range(10, 105, 5)]  # ratings 1.0 - 8.5

    movie = models.ForeignKey(Movie, related_name='votes', on_delete=models.CASCADE)
    rating = models.DecimalField(choices=PossibleRatings.RATES, max_digits=3, decimal_places=1)
    comment = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')
        verbose_name_plural = 'Oceny'
