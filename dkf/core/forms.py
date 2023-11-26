from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ten adres email jest już używany.')
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nazwa użytkownika:', widget=forms.TextInput(
        attrs={'placeholder': 'Twoja nazwa',
               'class': 'form-input'}
    ))
    password = forms.CharField(label='Hasło:', widget=forms.PasswordInput(
        attrs={'placeholder': 'Twoje hasło',
               'class': 'form-input'}))


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ('new_password1', 'new_password2')

    new_password1 = forms.CharField(label='Nowe hasło:', max_length=35, widget=forms.PasswordInput(
        attrs={'placeholder': 'Ustaw nowe hasło',
               'class': 'form-input'})
                                )

    new_password2 = forms.CharField(label='Powtórz nowe hasło:', max_length=35, widget=forms.PasswordInput(
        attrs={'placeholder': 'Powtórz nowe hasło',
               'class': 'form-input'})
                                )


class PasswordResetForm(PasswordResetForm):
    class Meta:
        fields = ('username', 'email')

    username = forms.CharField(label='Nazwa użytkownika:', widget=forms.TextInput(
        attrs={'placeholder': 'Twoja nazwa',
               'class': 'form-input'}
    ))

    email = forms.CharField(label='Email:', max_length=250, widget=forms.EmailInput(
        attrs={'placeholder': 'Twój adres email',
               'class': 'form-input'}))

