from django import forms
from .models import ServiceRequest

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['owner_name', 'pet_name', 'service_type', 'preferred_date', 'notes', 'sitter']
        widgets = {'preferred_date': forms.DateInput(attrs={'type': 'date'})}