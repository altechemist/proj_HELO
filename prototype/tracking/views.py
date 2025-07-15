from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import TrackingUpdate, Notification
from medications.models import MedicationOrder
from rides.models import RideRequest

@login_required
def tracking_dashboard(request):
    medication_orders = MedicationOrder.objects.filter(user=request.user).order_by('-created_at')[:5]
    ride_requests = RideRequest.objects.filter(user=request.user).order_by('-created_at')[:5]
    context = {
        'medication_orders': medication_orders,
        'ride_requests': ride_requests,
    }
    return render(request, 'tracking/dashboard.html', context)

@login_required
def medication_tracking(request, order_id):
    order = get_object_or_404(MedicationOrder, id=order_id, user=request.user)
    tracking_updates = order.tracking_updates.all().order_by('-created_at')
    context = {
        'order': order,
        'tracking_updates': tracking_updates,
    }
    return render(request, 'tracking/medication_tracking.html', context)

@login_required
def ride_tracking(request, ride_id):
    ride = get_object_or_404(RideRequest, id=ride_id, user=request.user)
    tracking_updates = ride.tracking_updates.all().order_by('-created_at')
    context = {
        'ride': ride,
        'tracking_updates': tracking_updates,
    }
    return render(request, 'tracking/ride_tracking.html', context)

@login_required
def tracking_update(request, service_type, service_id):
    if service_type == 'medication':
        service = get_object_or_404(MedicationOrder, id=service_id)
    elif service_type == 'ride':
        service = get_object_or_404(RideRequest, id=service_id)
    else:
        return JsonResponse({'error': 'Invalid service type'}, status=400)
    
    tracking_updates = service.tracking_updates.all().order_by('-created_at')
    updates_data = [{
        'status': update.status,
        'description': update.description,
        'latitude': float(update.latitude) if update.latitude else None,
        'longitude': float(update.longitude) if update.longitude else None,
        'estimated_arrival_time': update.estimated_arrival_time.isoformat() if update.estimated_arrival_time else None,
        'created_at': update.created_at.isoformat()
    } for update in tracking_updates]
    
    return JsonResponse({'updates': updates_data})

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'notifications': notifications,
    }
    return render(request, 'tracking/notification_list.html', context)

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect('tracking:notifications')

@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect('tracking:notifications')
