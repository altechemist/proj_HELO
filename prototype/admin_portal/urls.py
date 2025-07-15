from django.urls import path
from . import views

app_name = 'admin_portal'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('pharmacies/', views.pharmacy_list, name='pharmacy_list'),
    path('service-areas/', views.service_area_list, name='service_area_list'),
    path('logs/', views.admin_log_list, name='admin_log_list'),
] 