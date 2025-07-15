from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm, DriverProfileForm
from .models import UserProfile, Driver

# Create your views here.

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    context = {
        'profile': profile,
        'is_driver': hasattr(request.user, 'driver')
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def driver_registration(request):
    if hasattr(request.user, 'driver'):
        messages.warning(request, 'You are already registered as a driver.')
        return redirect('accounts:driver_dashboard')

    if request.method == 'POST':
        form = DriverProfileForm(request.POST, request.FILES)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.user = request.user
            driver.save()
            request.user.is_driver = True
            request.user.save()
            messages.success(request, 'You have successfully registered as a driver.')
            return redirect('accounts:driver_dashboard')
    else:
        form = DriverProfileForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/driver_registration.html', context)

@login_required
def driver_dashboard(request):
    if not request.user.is_driver:
        messages.warning(request, 'You need to register as a driver first.')
        return redirect('accounts:driver_registration')

    driver = request.user.driver
    active_rides = driver.assigned_rides.filter(status__in=['accepted', 'in_progress'])
    completed_rides = driver.assigned_rides.filter(status='completed')
    active_deliveries = driver.deliveries.filter(status__in=['confirmed', 'processing', 'out_for_delivery'])

    context = {
        'driver': driver,
        'active_rides': active_rides,
        'completed_rides': completed_rides,
        'active_deliveries': active_deliveries
    }
    return render(request, 'accounts/driver_dashboard.html', context)
