from . import views
from django.urls import path


app_name = 'event'

urlpatterns = [
   path('', views.get_all_events, name='all_events'),
   path('event-details/<int:pk>/', views.event_details, name='event_details'),
   path('new-event/', views.new_event, name='new_event'),
   path('edit-event/<int:pk>/', views.edit_event, name='edit_event'),
   path('delete-event/<int:pk>/', views.delete_event, name='delete_event'),
]
