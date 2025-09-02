
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

def validate_eafit_email(value:str):
    if not value.lower().endswith('@eafit.edu.co'):
        raise ValidationError('El correo debe ser @eafit.edu.co')

class User(AbstractUser):
    email = models.EmailField(unique=True, validators=[validate_eafit_email])
    def __str__(self): return f"@{self.username}"
