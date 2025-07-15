from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Hospital, Pharmacy, ServiceArea, AdminLog

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'hospitals_count': Hospital.objects.count(),
        'active_hospitals': Hospital.objects.filter(is_active=True).count(),
        'pharmacies_count': Pharmacy.objects.count(),
        'active_pharmacies': Pharmacy.objects.filter(is_active=True).count(),
        'service_areas_count': ServiceArea.objects.count(),
        'active_service_areas': ServiceArea.objects.filter(is_active=True).count(),
        'recent_logs': AdminLog.objects.order_by('-created_at')[:10]
    }
    return render(request, 'admin_portal/dashboard.html', context)

@user_passes_test(is_admin)
def hospital_list(request):
    hospitals = Hospital.objects.all().order_by('-created_at')
    return render(request, 'admin_portal/hospitals/list.html', {'hospitals': hospitals})

@user_passes_test(is_admin)
def pharmacy_list(request):
    pharmacies = Pharmacy.objects.all().order_by('-created_at')
    return render(request, 'admin_portal/pharmacies/list.html', {'pharmacies': pharmacies})

@user_passes_test(is_admin)
def service_area_list(request):
    areas = ServiceArea.objects.all().order_by('-created_at')
    return render(request, 'admin_portal/service_areas/list.html', {'areas': areas})

@user_passes_test(is_admin)
def admin_log_list(request):
    logs = AdminLog.objects.all().order_by('-created_at')
    return render(request, 'admin_portal/logs/list.html', {'logs': logs})
