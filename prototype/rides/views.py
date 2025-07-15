from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RideRequest, Ride

# Create your views here.

@login_required
def ride_list(request):
    available_rides = RideRequest.objects.filter(status='pending')
    context = {
        'rides': available_rides
    }
    return render(request, 'rides/ride_list.html', context)

@login_required
def book_ride(request):
    if request.method == "POST":
        pickup_location = request.POST.get("pickup_location")
        dropoff_location = request.POST.get("dropoff_location")
        pickup_time = request.POST.get("pickup_time")
        Ride.objects.create(
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            pickup_time=pickup_time,
        )
        return redirect("rides:ride_success")  # or wherever you want to redirect
    return render(request, "rides/book_ride.html")

@login_required
def ride_detail(request, ride_id):
    ride = get_object_or_404(RideRequest, id=ride_id, user=request.user)
    context = {
        'ride': ride
    }
    return render(request, 'rides/ride_detail.html', context)

@login_required
def ride_history(request):
    user_rides = RideRequest.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'rides': user_rides
    }
    return render(request, 'rides/ride_history.html', context)

@login_required
def cancel_ride(request, ride_id):
    ride = get_object_or_404(RideRequest, id=ride_id, user=request.user)
    if request.method == 'POST':
        ride.status = 'cancelled'
        ride.save()
        messages.success(request, 'Your ride has been cancelled successfully.')
        return redirect('rides:ride_history')
    return render(request, 'rides/cancel_ride.html', {'ride': ride})

def ride_success(request):
    return render(request, "rides/ride_success.html")