from django.shortcuts import render, redirect


def index(request):
    return render(request, 'core/index.html', {
        'title': 'Strona główna',
    })
