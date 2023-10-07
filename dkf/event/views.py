from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import EventForm
from .models import Event
from movie.models import Movie


def get_all_events(request):
    events = Event.objects.all()
    paginator = Paginator(events, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'event/all_events.html', {
        'events': events,
        'title': 'Wydarzenia',
        'page_obj': page_obj,})


def event_details(request, pk):
    event = get_object_or_404(Event, pk=pk)

    return render(request, 'event/event_details.html', {
        'event': event,
        'title': 'Szczegóły wydarzenia',})


@staff_member_required
def new_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event = event_form.save()
            existing_movies = event_form.cleaned_data['existing_movies']
            # Add existing movies to the event
            for movie_id in existing_movies:
                movie = Movie.objects.get(id=movie_id)
                event.movies.add(movie)
            event.save()
            return redirect('event:all_events')
    else:
        event_form = EventForm()

    return render(request, 'event/event_form.html', {
        'caption': 'Tworzenie nowego wydarzenia',
        'event_form': event_form,
        'title': 'Nowe wydarzenia',
    })


@staff_member_required
def edit_event(request, pk):
    print('hej')
    event = get_object_or_404(Event, pk=pk) if pk else None
    if request.method == 'POST':
        print('jol')
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            print('siema')
            event = event_form.save(commit=False)
            existing_movies = event_form.cleaned_data['existing_movies']
            event.movies.set(existing_movies)
            event_form.save()
            return redirect('event:all_events')
    else:
        print('cze')
        print("Initial movies:", event.movies.all())
        event_form = EventForm(instance=event, initial={'existing_movies': [
                movie.id for movie in event.movies.all()
        ]})

    print('juz')
    return render(request, 'event/event_form.html', {
        'caption': 'Edycja wydarzenia',
        'event_form': event_form,
        'event': event,
        'title': 'Edycja wydarzenia', })


@staff_member_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event:all_events')
    return render(request, 'event/delete_event.html', {
        'event': event,
        'title': 'Usuwanie wydarzenia', })
