from . import views
from django.urls import path


app_name = 'movie'
urlpatterns = [
    path('', views.get_all_movies, name='get_all_movies'),
]
