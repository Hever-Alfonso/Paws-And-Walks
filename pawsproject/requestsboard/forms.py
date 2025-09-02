
from django import forms
from .models import ServiceRequest

class RequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['title','service_type','description','contact_phone']
        widgets = {'description': forms.Textarea(attrs={'rows':4})}
