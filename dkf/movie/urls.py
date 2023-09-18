from . import views
from django.urls import path


app_name = 'movie'
urlpatterns = [
    path('', views.get_all_movies, name='get_all_movies'),
    path('details/<int:pk>/', views.movie_details, name='movie_details'),
    path('new-movie/', views.new_movie, name='new_movie'),
    path('delete-movie/<int:pk>/', views.delete_movie, name='delete_movie'),
    path('edit-movie/<int:pk>/', views.edit_movie, name='edit_movie'),
]
