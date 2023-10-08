from django.db import models
import datetime
from django.utils import timezone


class DateStatus(models.TextChoices):
    UNKNOWN = 'UNKNOWN', 'KIEDYŚ'
    NOW = 'NOW', 'TERAZ'
    PAST = 'PAST', 'BYŁO'
    FUTURE = 'FUTURE', 'BĘDZIE'


class Event(models.Model):
    description = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    date_status = models.CharField(max_length=8,
                                   choices=DateStatus.choices,
                                   default=DateStatus.UNKNOWN, blank=True, null=True)
    location = models.CharField(max_length=255, default='inne - podaj / kino nowe horyzonty / budynek A1 PWR, sala 329')
    movies = models.ManyToManyField('movie.Movie', blank=True, related_name='events')
    time = models.TimeField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = 'Nasze wydarzenia'

    def event_in_current_week(self) -> bool:
        current_year = datetime.date.today().year
        current_week = datetime.date.today().isocalendar().week
        event_year = self.date.year
        event_week = self.date.isocalendar().week
        return current_week == event_week and current_year == event_year

    def event_in_past(self) -> bool:
        current_year = datetime.date.today().year
        current_week = datetime.date.today().isocalendar().week
        event_year = self.date.year
        event_week = self.date.isocalendar().week
        result = current_week > event_week and current_year == event_year
        return current_year > event_year or result

    def event_in_future(self) -> bool:
        current_year = datetime.date.today().year
        current_week = datetime.date.today().isocalendar().week
        event_year = self.date.year
        event_week = self.date.isocalendar().week
        result = current_week < event_week and current_year == event_year
        return current_year <= event_year or result

    def __str__(self) -> str:
        formatted_date = self.date.strftime('%d.%m.%y')
        formatted_time = self.time.strftime('%H:%M')
        return f'{formatted_date} - {formatted_time}'
