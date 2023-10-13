from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import login_required
from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from .forms import MovieForm, VoteForm
from .models import Movie, Vote


def get_all_movies(request):
    movies = Movie.objects.all()
    votes = Vote.objects.all()
    rated_movies = {}

    for movie in movies:
        rate = Vote.objects.filter(movie__title=movie.title).aggregate(Avg("rating"))['rating__avg']
        rated_movies.update({movie: rate})

    for key, value in rated_movies.items():
        print(f"Key: {key}, Value: {value}")

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


@staff_member_required
def new_movie(request):
    form_url = request.path
    print(form_url)

    if request.method == 'POST':
        movie_form = MovieForm(request.POST, request.FILES)

        if movie_form.is_valid():
            movie = movie_form.save(commit=False)
            movie.save()

            return redirect('movie:get_all_movies')

    else:
        movie_form = MovieForm()

    return render(request, 'movie/new_movie.html', {
        'movie_form': movie_form,
        'title': 'Nowy film',
        'caption': 'Tworzenie nowego filmu',
    })


@staff_member_required
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('/')
    return render(request, 'movie/delete_movie.html', {
        'movie': movie,
        'title': 'Usuwanie filmu',
    })


@staff_member_required
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk) if pk else None
    if request.method == 'POST':
        movie_form = MovieForm(request.POST, instance=movie)
        if movie_form.is_valid():
            movie_form.save()
            return redirect('movie:get_all_movies')
    else:
        movie_form = MovieForm(instance=movie)
    return render(request, 'movie/new_movie.html', {
        'movie_form': movie_form,
        'movie': movie,
        'title': 'Edycja filmu',
        'caption': 'Edycja filmu',
    })


@login_required
def new_vote(request, pk):
    movie = get_object_or_404(Movie, pk=pk) if pk else None

    if request.method == 'POST':
        vote_form = VoteForm(request.POST)
        if vote_form.is_valid():
            vote = vote_form.save(commit=False)
            vote.movie = movie
            vote.user = request.user
            vote.save()
            return redirect('movie:get_all_movies')

    else:
        vote_form = VoteForm()

    return render(request, 'movie/vote_form.html', {
        'caption': 'Ocena filmu',
        'movie': movie,
        'vote_form': vote_form,
    })


@login_required
def edit_vote(request, pk):
    vote = get_object_or_404(Vote, pk=pk) if pk else None

    if vote.user != request.user:
        raise Http404("Nie masz uprawnień do tego elementu.")

    movie = vote.movie if vote else None

    if request.method == 'POST':
        vote_form = VoteForm(request.POST, instance=vote)
        if vote_form.is_valid():
            vote_form.save()
            return redirect('movie:get_all_movies')
    else:
        vote_form = VoteForm(instance=vote)
    return render(request, 'movie/vote_form.html', {
        'caption': 'Edycja oceny',
        'movie': movie,
        'vote_form': vote_form,
        'title': 'Edycja oceny',
    })


@login_required
def get_user_votes(request):
    current_user = request.user
    all_votes = Vote.objects.all()
    votes = Vote.objects.filter(user=current_user)
    user_votes = {}
    for vote in votes:
        movie = vote.movie
        average_rate = all_votes.filter(movie__title=movie.title).aggregate(Avg("rating"))['rating__avg']
        average_rate = f'{average_rate: .1f}'
        user_votes.update({vote: average_rate})

    rated_list = list(user_votes.items())
    paginator = Paginator(rated_list, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'movie/user_votes.html', {
        'page_obj': page_obj,
        'title': 'Twoje oceny',
        'user_votes': user_votes,
    })
