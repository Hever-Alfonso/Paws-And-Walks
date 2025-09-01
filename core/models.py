from django.db import models

class Sitter(models.Model):
    name = models.CharField(max_length=80)
    bio = models.TextField(blank=True)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)
    availability_notes = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.name

SERVICE_TYPES = [
    ('walk', 'Walking'),
    ('care', 'Pet Care'),
]

class ServiceRequest(models.Model):
    owner_name = models.CharField(max_length=80)
    pet_name = models.CharField(max_length=80)
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPES)
    preferred_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    sitter = models.ForeignKey(Sitter, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner_name} → {self.service_type} ({self.pet_name})"