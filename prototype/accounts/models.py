from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True)
    address = models.TextField(blank=True)
    is_driver = models.BooleanField(default=False)
    is_medical_staff = models.BooleanField(default=False)
    is_pharmacy_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    emergency_contact = PhoneNumberField(blank=True)
    medical_conditions = models.TextField(blank=True)
    preferred_hospital = models.CharField(max_length=255, blank=True)
    preferred_pharmacy = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"

class Driver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='driver')
    vehicle_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50)
    medical_training_cert = models.FileField(upload_to='driver_certs/', blank=True)
    current_location = models.CharField(max_length=255, blank=True)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)

    def __str__(self):
        return f"Driver: {self.user.get_full_name()}"
