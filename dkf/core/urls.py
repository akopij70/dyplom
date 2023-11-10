from django.urls import path
from .forms import LoginForm
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html', next_page=None), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('change-password', views.change_password, name='change_password'),
    path('reset-password', views.reset_password, name='reset_password'),
    path('reset/<uidb64>/<token>', views.reset_password_confirm, name='reset_password_confirm'),
]
