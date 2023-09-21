from . import views
from django.urls import path


app_name = 'event'

urlpatterns = [
   path('', views.get_all_events, name='all_events'),
   path('event-details/<int:pk>/', views.event_details, name='event_details'),
]
