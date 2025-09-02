
from django import forms
from .models import SitterProfile, SitterService, SitterRating
class SitterProfileForm(forms.ModelForm):
    class Meta: model = SitterProfile; fields = ['bio','phone','photo']
class SitterServiceForm(forms.ModelForm):
    class Meta: model = SitterService; fields = ['service_type','price_cop']
class RatingForm(forms.ModelForm):
    class Meta:
        model = SitterRating; fields = ['score','comment']
        widgets = {'score': forms.NumberInput(attrs={'min':1,'max':5})}
