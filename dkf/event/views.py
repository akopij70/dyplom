from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Event


def get_all_events(request):
    events = Event.objects.all()
    paginator = Paginator(events, 5)

    for event in events:
        for movie in event.movies.all():
            print('jo')

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'event/all_events.html', {
        'title': 'Wydarzenia',
        'events': events,
        'page_obj': page_obj,
    })
