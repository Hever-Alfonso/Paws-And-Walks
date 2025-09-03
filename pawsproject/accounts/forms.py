from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ROLE_CHOICES

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Register as')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={'placeholder':'tuusuario@eafit.edu.co'})
        self.fields['email'].help_text = 'Debes usar tu correo institucional @eafit.edu.co'
        self.fields['password1'].help_text = 'Mínimo 8 caracteres, incluir mayúscula, minúscula y número.'
        self.fields['password2'].help_text = 'Repítela para confirmar.'

    class Meta:
        model = User
        fields = ('username','email','role')

    def clean_password2(self):
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')
        if pwd1 != pwd2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        # Basic policy: at least 8 chars, one uppercase, one lowercase, one digit
        import re
        if not re.search(r'[A-Z]', pwd1) or not re.search(r'[a-z]', pwd1) or not re.search(r'\d', pwd1) or len(pwd1) < 8:
            raise forms.ValidationError('La contraseña debe tener mínimo 8 caracteres, incluir mayúscula, minúscula y número.')
        return pwd2
