from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from .models import Movie, Vote


def get_all_movies(request):
    movies = Movie.objects.all()
    votes = Vote.objects.all()
    rated_movies = {}

    for movie in movies:
        rate = Vote.objects.filter(movie__title=movie.title).aggregate(Avg("rating"))['rating__avg']
        rated_movies.update({movie: rate})

    # for key, value in rated_movies.items():
    #     print(f"Key: {key}, Value: {value}")

    rated_list = list(rated_movies.items())
    paginator = Paginator(rated_list, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'movie/all_movies.html', {
        'rated_movies': rated_movies,
        'title': 'Filmy',
        'movies': movies,
        'votes': votes,
        'page_obj': page_obj,

    })

def movie_details(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movie/movie_details.html', {
        'movie': movie,
        'title': 'Szczegóły filmu',
    })
