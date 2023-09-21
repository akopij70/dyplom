from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Event


def get_all_events(request):
    events = Event.objects.all()
    paginator = Paginator(events, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'event/all_events.html', {
        'title': 'Wydarzenia',
        'events': events,
        'page_obj': page_obj,
    })


def event_details(request, pk):
    event = get_object_or_404(Event, pk=pk)

    return render(request, 'event/event_details.html', {
        'title': 'Szczegóły wydarzenia',
        'event': event,
    })
