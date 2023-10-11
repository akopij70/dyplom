from django import forms
from django.utils.html import format_html
from .models import Movie, Vote


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


# class ImageSelect(forms.widgets.Select):
#     def render_option(self, selected_choices, option_value, option_label, option_index, subwidgets):
#         html = super().render_option(selected_choices, option_value, option_label, option_index, subwidgets)
#         image_path = f'rates/{option_label}.png'  # Replace with the actual path to your images
#         image_html = format_html(
#             '<label class="image-label"><img src="{}" alt="{}" /><br>{}</label>',
#             image_path,
#             option_label,
#             html,
#         )
#         return format_html('{} {}', image_html, html)


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['comment', 'rating']

    comment = forms.CharField(label='Twój komentarz (opcjonalny)',
                              required=False, max_length=255,
                              widget=forms.Textarea(attrs={'class': 'form-input'}))

    # rating = forms.ChoiceField(choices=Vote.PossibleRatings.RATES, label='Twoja ocena',
    #                            widget=forms.Select(attrs={'class': 'form-input'}))

    rating = forms.DecimalField(label='Twoja ocena', widget=forms.HiddenInput())
        
    # rating = forms.ChoiceField(choices=Vote.PossibleRatings.RATES, label='Twoja ocena',
    #                            widget=ImageSelect(attrs={'class': ''}))
