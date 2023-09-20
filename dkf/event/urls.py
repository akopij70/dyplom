from . import views
from django.urls import path


app_name = 'event'

urlpatterns = [
   path('', views.get_all_events, name='all_events'),
]
