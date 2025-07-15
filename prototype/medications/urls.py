from django.urls import path
from . import views

app_name = 'medications'

urlpatterns = [
    path('', views.medication_list, name='list'),
    path('order/', views.order_medication, name='order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('prescriptions/', views.prescription_list, name='prescriptions'),
    path('prescriptions/upload/', views.upload_prescription, name='upload_prescription'),
] 