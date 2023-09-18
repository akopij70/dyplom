from django import forms
from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'director', 'release_date', 'description', 'thumbnail']

    title = forms.CharField(label='Tytuł:', widget=forms.TextInput(
        attrs={'placeholder': 'Tytuł filmu bez cudzysłowów',
               'class': 'form-input'}))

    director = forms.CharField(label='Reżyser:', widget=forms.TextInput(
        attrs={'class': 'form-input'}))

    release_date = forms.IntegerField(min_value=1, label='Rok premiery:', required=False, widget=forms.NumberInput(
        attrs={'class': 'form-input'}))

    description = forms.CharField(label='Opis:', required=False, widget=forms.Textarea(
        attrs={'class': 'form-input'}))

    thumbnail = forms.FileField(label='Miniaturka', required=False,
                                widget=forms.FileInput(attrs={'class': 'form-input'}))
