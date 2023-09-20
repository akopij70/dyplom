from django.shortcuts import render, redirect
from .forms import SignupForm
from event.models import Event, DateStatus


def index(request):
    past_events = []
    future_events = []
    sorted_events = []

    events = Event.objects.all()
    for event in events:
        print(event.date)
        if event.event_in_current_week():
            event.date_status = DateStatus.NOW
            sorted_events.append(event)
        elif event.event_in_past():
            print("BYLO")
            event.date_status = DateStatus.PAST
            past_events.append(event)
        elif event.event_in_future():
            event.date_status = DateStatus.FUTURE
            future_events.append(event)

        event.save()
        if len(past_events) == 5:
            break

    if len(future_events) > 5:
        sorted_events.extend(future_events[-5])  # bo domyslnie im nowsze wydarzenie tym wyzej
    else:
        sorted_events.extend(future_events)

    if len(past_events) > 5:
        sorted_events.extend(past_events[0:5])  # bo domyslnie im nowsze wydarzenie tym wyzej
    else:
        sorted_events.extend(past_events)

    return render(request, 'core/index.html', {
        'title': 'Strona główna',
        'all_events': events,
        'past_events': past_events,
        'current_events': sorted_events,
        'future_events': future_events,
    })


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignupForm
    return render(request, 'core/signup.html', {
        'form': form
    })
