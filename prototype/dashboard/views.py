from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from medications.models import MedicationOrder
from rides.models import RideRequest
from tracking.models import TrackingUpdate
from itertools import chain
from operator import attrgetter

@login_required
def home(request):
    # Get active rides
    active_rides = RideRequest.objects.filter(
        user=request.user,
        status__in=['pending', 'accepted', 'in_progress']
    ).order_by('-created_at')[:5]

    # Get active medication orders
    active_orders = MedicationOrder.objects.filter(
        user=request.user,
        status__in=['pending', 'confirmed', 'processing', 'out_for_delivery']
    ).order_by('-created_at')[:5]

    # Get recent activities
    ride_updates = TrackingUpdate.objects.filter(
        ride_request__user=request.user
    ).select_related('ride_request')

    medication_updates = TrackingUpdate.objects.filter(
        medication_order__user=request.user
    ).select_related('medication_order')

    # Combine and sort activities
    recent_activities = sorted(
        chain(ride_updates, medication_updates),
        key=attrgetter('created_at'),
        reverse=True
    )[:10]

    # Get upcoming events
    upcoming_rides = RideRequest.objects.filter(
        user=request.user,
        pickup_time__gt=timezone.now()
    ).order_by('pickup_time')[:5]

    upcoming_deliveries = MedicationOrder.objects.filter(
        user=request.user,
        scheduled_delivery__gt=timezone.now()
    ).order_by('scheduled_delivery')[:5]

    # Combine and sort upcoming events
    upcoming_events = []
    for ride in upcoming_rides:
        upcoming_events.append({
            'type': 'ride',
            'title': f'Ride to {ride.dropoff_location}',
            'scheduled_time': ride.pickup_time
        })

    for delivery in upcoming_deliveries:
        upcoming_events.append({
            'type': 'delivery',
            'title': f'Medication Delivery',
            'scheduled_time': delivery.scheduled_delivery
        })

    upcoming_events.sort(key=lambda x: x['scheduled_time'])

    context = {
        'active_rides': active_rides,
        'active_orders': active_orders,
        'recent_activities': recent_activities,
        'upcoming_events': upcoming_events
    }

    return render(request, 'dashboard/home.html', context)
