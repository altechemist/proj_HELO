from django.db import models
from django.conf import settings
from medications.models import MedicationOrder
from rides.models import RideRequest

class TrackingUpdate(models.Model):
    STATUS_CHOICES = [
        ('initiated', 'Service Initiated'),
        ('processing', 'Processing'),
        ('assigned', 'Assigned to Driver'),
        ('in_transit', 'In Transit'),
        ('near_location', 'Near Location'),
        ('arrived', 'Arrived'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    medication_order = models.ForeignKey(MedicationOrder, on_delete=models.CASCADE, null=True, blank=True, related_name='tracking_updates')
    ride_request = models.ForeignKey(RideRequest, on_delete=models.CASCADE, null=True, blank=True, related_name='tracking_updates')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description = models.TextField()
    estimated_arrival_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        service = self.medication_order or self.ride_request
        return f"Update for {service.__class__.__name__} #{service.id}"

class Notification(models.Model):
    TYPE_CHOICES = [
        ('status_update', 'Status Update'),
        ('reminder', 'Reminder'),
        ('alert', 'Alert'),
        ('info', 'Information')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tracking_notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    medication_order = models.ForeignKey(MedicationOrder, on_delete=models.CASCADE, null=True, blank=True)
    ride_request = models.ForeignKey(RideRequest, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.get_full_name()} - {self.title}"
