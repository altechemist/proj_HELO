from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    # Ticket management
    path('', views.ticket_list, name='ticket_list'),
    path('ticket/new/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<int:ticket_id>/update/', views.update_ticket, name='update_ticket'),
    path('ticket/<int:ticket_id>/close/', views.close_ticket, name='close_ticket'),
    
    # Messages
    path('ticket/<int:ticket_id>/message/', views.add_message, name='add_message'),
    path('ticket/<int:ticket_id>/message/<int:message_id>/attachment/', 
         views.download_attachment, name='download_attachment'),
    
    # Feedback
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('feedback/new/', views.create_feedback, name='create_feedback'),
    path('feedback/<int:feedback_id>/', views.feedback_detail, name='feedback_detail'),
] 