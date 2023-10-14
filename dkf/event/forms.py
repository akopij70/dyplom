from django import forms
from movie.models import Movie

from .models import Event


def get_existing_movies():
    return [(movie.id, movie.title) for movie in Movie.objects.all()]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['existing_movies', 'date', 'time', 'location', 'title', 'description']

    existing_movies = forms.MultipleChoiceField(
        label='Film(y) na wydarzeniu',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-input'}),
        required=False,
        choices=get_existing_movies(),
    )

    date = forms.DateField(
        label='Data',
        widget=forms.TextInput(attrs={'class': 'form-input', 'type': 'date'}),
    )

    time = forms.TimeField(label='Godzina',
                           widget=forms.TimeInput(attrs={'placeholder': 'HH:MM', 'class': 'form-input'})
                           )

    location = forms.CharField(label='Miejsce',
                               initial='inne - podaj / kino nowe horyzonty / budynek A1 PWR, sala 329',
                               widget=forms.TextInput(attrs={'class': 'form-input',
                                                             'placeholder': 'inne - podaj / kino nowe horyzonty / '
                                                                            'budynek A1 PWR, sala 329'})
                               )

    title = forms.CharField(label='Nazwa wydarzenia - zostaw puste aby po prostu wyświetlać tytuły filmów z wydarzenia',
                            required=False, widget=forms.TextInput(attrs={'class': 'form-input'})
                            )

    description = forms.CharField(label='Opis wydarzenia', required=False, widget=forms.Textarea(
        attrs={'class': 'form-input'})
                                  )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['existing_movies'].choices = get_existing_movies()
