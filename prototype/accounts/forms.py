from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm
from .models import CustomUser, UserProfile, Driver

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'address')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'address')

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.address = self.cleaned_data['address']
        user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'emergency_contact', 'medical_conditions', 
                 'preferred_hospital', 'preferred_pharmacy')
        widgets = {
            'medical_conditions': forms.Textarea(attrs={'rows': 3}),
        }

class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('vehicle_number', 'vehicle_type', 'license_number', 'medical_training_cert')
        widgets = {
            'vehicle_type': forms.Select(choices=[
                ('sedan', 'Sedan'),
                ('suv', 'SUV'),
                ('van', 'Van'),
                ('ambulance', 'Ambulance')
            ])
        } 