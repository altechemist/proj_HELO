from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    # Tracking endpoints
    path('', views.tracking_dashboard, name='dashboard'),
    path('medication/<int:order_id>/', views.medication_tracking, name='medication_tracking'),
    path('ride/<int:ride_id>/', views.ride_tracking, name='ride_tracking'),
    path('update/<str:service_type>/<int:service_id>/', views.tracking_update, name='update'),
    
    # Notification endpoints
    path('notifications/', views.notification_list, name='notifications'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
] 
 