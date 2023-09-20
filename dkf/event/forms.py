from django import forms
from dkf.movie.models import Movie
from models import Event


class EventForm(forms.ModelForm):
    existing_movies = forms.MultipleChoiceField(
        label='Filmy, które mamy w bazie:',
        choices=[(movie.id, movie.title) for movie in Movie.objects.all()],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'new_event_selector'}),
    )

    class Meta:
        model = Event
        fields = ['date', 'time', 'location', 'description', 'existing_movies']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['existing_movies'].choices = self.get_existing_movies()

    def get_existing_movies(self):
        return [(movie.id, movie.title) for movie in Movie.objects.all()]

    date = forms.DateField(label='Data:', widget=forms.DateInput(attrs={
        'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
        'class': 'form-input'
    }))

    time = forms.TimeField(label='Godzina:',
                           widget=forms.TimeInput(attrs={'placeholder': 'HH:MM', 'class': 'form-input'})
                           )

    location = forms.CharField(label='Miejsce:',
                               initial='inne - podaj / kino nowe horyzonty / budynek A1 PWR, sala 329',
                               widget=forms.TextInput(attrs={'class': 'form-input',
                                                             'placeholder': 'inne - podaj / kino nowe horyzonty / '
                                                                            'budynek A1 PWR, sala 329'}))

    description = forms.CharField(label='Opis wydarzenia:', required=False, widget=forms.Textarea(
        attrs={'class': 'form-input'}))
