
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
SERVICE_CHOICES = [('walk','Dog Walk'), ('care','Pet Care'), ('train','Training')]

class ServiceRequest(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    title = models.CharField(max_length=120)
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES)
    description = models.TextField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self): return f"{self.title} [{self.get_service_type_display()}]"
