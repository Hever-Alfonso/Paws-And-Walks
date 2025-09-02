
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

User = settings.AUTH_USER_MODEL
SERVICE_CHOICES = [('walk','Dog Walk'), ('care','Pet Care')]

class SitterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sitter_profile')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    average_rating = models.FloatField(default=0.0)
    ratings_count = models.PositiveIntegerField(default=0)
    def __str__(self): return f"{self.user}"

class SitterService(models.Model):
    profile = models.ForeignKey(SitterProfile, on_delete=models.CASCADE, related_name='services')
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES)
    price_cop = models.PositiveIntegerField(default=0)
    class Meta:
        unique_together = ('profile','service_type')
    def __str__(self): return f"{self.profile.user} - {self.get_service_type_display()} ({self.price_cop})"

class SitterRating(models.Model):
    profile = models.ForeignKey(SitterProfile, on_delete=models.CASCADE, related_name='ratings')
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('profile','rater')
        ordering = ['-created_at']
    def __str__(self): return f"Rating({self.profile.user} <- {self.rater}: {self.score})"
