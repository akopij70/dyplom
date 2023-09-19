from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(label='Nazwa użytkownika:', max_length=35, widget=forms.TextInput(
        attrs={'placeholder': 'Twoja nazwa',
               'class': 'form-input'}))

    email = forms.CharField(label='Email:', max_length=250, widget=forms.EmailInput(
        attrs={'placeholder': 'Twój adres email',
               'class': 'form-input'}))

    password1 = forms.CharField(label='Hasło:', max_length=35, widget=forms.PasswordInput(
        attrs={'placeholder': 'Ustaw hasło',
               'class': 'form-input'})
                                )

    password2 = forms.CharField(label='Powtórz hasło:', max_length=35, widget=forms.PasswordInput(
        attrs={'placeholder': 'Powtórz hasło',
               'class': 'form-input'})
                                )


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nazwa użytkownika:', widget=forms.TextInput(
        attrs={'placeholder': 'Twoja nazwa',
               'class': 'form-input'}
    ))
    password = forms.CharField(label='Hasło:', widget=forms.PasswordInput(
        attrs={'placeholder': 'Twoje hasło',
               'class': 'form-input'}))
