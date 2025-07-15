from django.urls import path
from . import views

app_name = 'rides'

urlpatterns = [
    path('', views.ride_list, name='list'),
    path('book/', views.book_ride, name='book'),
    path('ride/<int:ride_id>/', views.ride_detail, name='ride_detail'),
    path('history/', views.ride_history, name='history'),
    path('cancel/<int:ride_id>/', views.cancel_ride, name='cancel'),
    path('history/', views.ride_history, name='ride_history'),
    path('success/', views.ride_success, name='ride_success'),
] 