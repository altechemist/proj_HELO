from django import forms
from .models import MedicationOrder, Prescription

class MedicationOrderForm(forms.ModelForm):
    class Meta:
        model = MedicationOrder
        fields = ['medications', 'delivery_address', 'delivery_instructions', 'scheduled_delivery']
        widgets = {
            'scheduled_delivery': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'delivery_instructions': forms.Textarea(attrs={'rows': 3}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication', 'doctor_name', 'hospital_name', 'prescription_date', 
                 'expiry_date', 'prescription_image']
        widgets = {
            'prescription_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        } 