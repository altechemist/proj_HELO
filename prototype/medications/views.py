from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medication, MedicationOrder, Prescription
from .forms import MedicationOrderForm, PrescriptionForm

# Create your views here.

@login_required
def medication_list(request):
    medications = Medication.objects.filter(stock__gt=0)
    context = {
        'medications': medications
    }
    return render(request, 'medications/medication_list.html', context)

@login_required
def order_medication(request):
    if request.method == 'POST':
        form = MedicationOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Your medication order has been placed successfully.')
            return redirect('medications:order_detail', order_id=order.id)
    else:
        form = MedicationOrderForm()
    
    context = {
        'form': form
    }
    return render(request, 'medications/order_form.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(MedicationOrder, id=order_id, user=request.user)
    context = {
        'order': order
    }
    return render(request, 'medications/order_detail.html', context)

@login_required
def prescription_list(request):
    prescriptions = Prescription.objects.filter(user=request.user)
    context = {
        'prescriptions': prescriptions
    }
    return render(request, 'medications/prescription_list.html', context)

@login_required
def upload_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.user = request.user
            prescription.save()
            messages.success(request, 'Your prescription has been uploaded successfully.')
            return redirect('medications:prescriptions')
    else:
        form = PrescriptionForm()
    
    context = {
        'form': form
    }
    return render(request, 'medications/prescription_form.html', context)
