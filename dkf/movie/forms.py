from django import forms
from django.utils.html import format_html
from .models import Movie, Vote


class FilterRanges:
    PossibleRates = [
        (0, 0, '---'),
        (1, 2, 'do 2'),
        (2, 3, '2 - 3'),
        (3, 4, '3 - 4'),
        (4, 5, '4 - 5'),
        (5, 6, '5 - 6'),
        (6, 7, '6 - 7'),
        (7, 8, '7 - 8'),
        (8, 9, '8 - 9'),
        (9, 10, 'od 9'),
    ]

    PossibleYears = [
        (0, 0, '---'),
        (0, 1950, 'przed 1950'),
        (1950, 1960, '1950-1960'),
        (1960, 1970, '1960-1970'),
        (1970, 1980, '1970-1980'),
        (1980, 1990, '1980-1990'),
        (1990, 2000, '1990-2000'),
        (2000, 2010, '2000-2010'),
        (2010, 2020, '2010-2020'),
        (2020, 2040, 'po 2020'),
    ]


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


class MovieFilterForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = ['title', 'director', 'rating', 'year']

    class RateRangeField(forms.IntegerField):
        widget = forms.Select(
            choices=[(i, FilterRanges.PossibleRates[i][2]) for i in range(len(FilterRanges.PossibleRates))],
            attrs={'class': 'filter-select'})

    class YearRangeField(forms.IntegerField):
        widget = forms.Select(
            choices=[(i, FilterRanges.PossibleYears[i][2]) for i in range(len(FilterRanges.PossibleYears))],
            attrs={'class': 'filter-select'})

    title = director = forms.CharField(label='Tytuł', max_length=255, required=False,
                                       widget=forms.TextInput(attrs={'class': 'search-input',
                                                                     'placeholder': 'Wyszukaj film'}))
    director = forms.CharField(label='Reżyser', max_length=255, required=False,
                               widget=forms.TextInput(attrs={'class': 'filter-input'}))
    rating = RateRangeField(label='Ocena widzów', required=False)
    year = YearRangeField(label='Rok premiery', required=False)


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['comment', 'rating']

    comment = forms.CharField(label='Twój komentarz (opcjonalny)',
                              required=False, max_length=255,
                              widget=forms.Textarea(attrs={'class': 'form-input'}))

    rating = forms.DecimalField(label='Twoja ocena', widget=forms.HiddenInput())


