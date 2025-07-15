from django.db import models
from django.conf import settings
from django.utils import timezone

class Ride(models.Model):
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    pickup_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class RideRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    RIDE_TYPE_CHOICES = [
        ('standard', 'Standard'),
        ('wheelchair', 'Wheelchair Accessible'),
        ('stretcher', 'Stretcher'),
        ('medical_escort', 'Medical Escort')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ride_requests')
    pickup_location = models.TextField()
    dropoff_location = models.TextField()
    pickup_time = models.DateTimeField()
    ride_type = models.CharField(max_length=20, choices=RIDE_TYPE_CHOICES, default='standard')
    special_instructions = models.TextField(blank=True)
    medical_assistance_required = models.BooleanField(default=False)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_rides')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    estimated_fare = models.DecimalField(max_digits=10, decimal_places=2)
    actual_fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride #{self.id} - {self.user.get_full_name()}"

class RideLocation(models.Model):
    ride = models.ForeignKey(RideRequest, on_delete=models.CASCADE, related_name='locations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    location_type = models.CharField(max_length=20, choices=[('pickup', 'Pickup'), ('dropoff', 'Dropoff'), ('current', 'Current')])

    def __str__(self):
        return f"{self.ride.id} - {self.location_type} at {self.timestamp}"

class RideReview(models.Model):
    ride = models.OneToOneField(RideRequest, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Ride #{self.ride.id}"
