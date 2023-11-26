from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from event.models import Event, DateStatus

from .tokens import generate_token

from .forms import PasswordResetForm, SetPasswordForm, SignupForm


def index(request):
    past_events = []
    future_events = []
    sorted_events = []

    events = Event.objects.all()
    for event in events:
        # print(event.date)
        if event.event_in_current_week():
            event.date_status = DateStatus.NOW
            sorted_events.append(event)
        elif event.event_in_past():
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


def contact(request):
    return render(request, 'core/contact.html')

# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/login/')
#     else:
#         form = SignupForm
#     return render(request, 'core/signup.html', {
#         'form': form
#     })
# def activate_email(request, user, to_email):
#     messages.success(request, f'Użytkowniku: <b>{user}</b>, proszę sprawdź swoją pocztę <b>{to_email}</b> i \
#         kliknij w otrzymany link, w celu aktywacji konta. <b>Uwaga:</b> Sprawdź folder ze spamem.')


def activate_email(request, user, to_email):
    mail_subject = 'Aktywacja konta użytkownika'
    message = render_to_string('core/activate_account.html', {
        'username': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Użytkowniku <b>{user}</b>, sprawdź swoją pocztę <b>{to_email}</b> i \
                kliknij otrzymany link, aby aktywować konto. Jeżeli nie widzisz nowej wiadomości, sprawdź folder ze spamem.')

    else:
        messages.error(request, f'Problem z wysłaniem maila do {to_email}, sprawdź poprawność adresu.')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # form.clean_email()
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            return redirect('/')
    else:
        form = SignupForm
    return render(request, 'core/signup.html', {
            'form': form
        })


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Dziękujemy za potwierdzenie adresu email. Teraz możesz się zalogować.')
        return redirect('core:login')
    else:
        messages.error(request, 'Link jest niepoprawny!')

    return redirect('/')


# @login_required
# def change_password(request):
#     user = request.user
#     if request.method == 'POST':
#         form = SetPasswordForm(user, request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('core:logout')
#
#     form = SetPasswordForm(user)
#
#     return render(request, 'core/change_password.html', {
#         'form': form,
#         'title': 'Edycja hasła',
#         'caption': 'Edycja hasła',
#     })


@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Zmieniono hasło!")
            return redirect('core:logout')
    else:
        form = SetPasswordForm(user)

    return render(request, 'core/change_password.html', {
        'form': form,
        'title': 'Edycja hasła',
        'caption': 'Edycja hasła',
    })


def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            name = form.cleaned_data['username']
            # associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            associated_user = get_user_model().objects.filter(email=user_email, username=name).first()
            if associated_user:
                subject = 'Zmiana hasła'
                message = render_to_string('core/reset_password_email.html', {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': generate_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                                     """
                                     Jeżeli podano prawidłowy adres email, wiadomość z instrukcjami została wysłana.
                                     Powinna pojawić się szybko, jeżeli to nie nastąpi, sprawdź  folder spam i 
                                     poprawność adresu email.
                                     """
                                     )
                else:
                    messages.error(request, "Problem z wysłaniem wiadomości, <b>SERVER PROBLEM</b>")
            else:
                messages.success(request,
                                 """
                                 Jeżeli podano prawidłowy adres email, wiadomość z instrukcjami została wysłana.
                                 Powinna pojawić się szybko, jeżeli to nie nastąpi, sprawdź  folder spam i 
                                 poprawność adresu email.
                                 """
                                 )

            return redirect('core:index')

    else:
        form = PasswordResetForm()

    return render(
        request, 'core/reset_password.html', {
            'caption': 'Reset hasła',
            'form': form,
            'title': 'Reset hasła'})


def reset_password_confirm(request, uidb64, token):

    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and generate_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Twoje hasło zostało zmienione, możesz się zalogować.")
                return redirect('core:logout')
        else:
            form = SetPasswordForm(user)
        return render(request, 'core/change_password.html', {
            'form': form,
            'title': 'Reset hasła',
            'caption': 'Podaj nowe hasło',
        })
    else:
        messages.error(request, "Link stracił ważność")

    messages.error(request, 'Coś poszło nie tak, powrót na stronę główną')
    return redirect('core:index')
