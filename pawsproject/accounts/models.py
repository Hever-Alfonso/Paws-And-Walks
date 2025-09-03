
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

def validate_eafit_email(value:str):
    if not value.lower().endswith('@eafit.edu.co'):
        raise ValidationError('El correo debe ser @eafit.edu.co')

# Added role-based access: users can be 'owner', 'sitter', or 'both'.
ROLE_CHOICES = (('owner','Owner'), ('sitter','Sitter'), ('both','Both'))

class User(AbstractUser):
    # English comments by request
    # Enforce institutional email and add a role field for access control.
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='owner')

    email = models.EmailField(unique=True, validators=[validate_eafit_email])
    def __str__(self): return f"@{self.username}"
    # Convenience helpers
    @property
    def is_owner(self): return self.role in ('owner','both')
    @property
    def is_sitter(self): return self.role in ('sitter','both')
