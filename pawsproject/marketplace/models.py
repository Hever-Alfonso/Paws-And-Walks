from PIL import Image

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
    

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    # Resize uploaded profile photo to a sane size (max 800x800) to avoid huge files on page
    if self.photo and hasattr(self.photo, 'path'):
        try:
            img = Image.open(self.photo.path)
            MAX_SIZE = (800, 800)
            if img.height > MAX_SIZE[1] or img.width > MAX_SIZE[0]:
                img.thumbnail(MAX_SIZE)  # in-place, keeps aspect ratio
                img.save(self.photo.path, optimize=True, quality=85)
        except Exception:
            # If resizing fails, we silently ignore to not block user actions
            pass
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

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    sitter_profile = models.ForeignKey(SitterProfile, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.content[:30]}"
    
    from django.utils import timezone

class Appointment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_owner')
    sitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_sitter')
    sitter_profile = models.ForeignKey(SitterProfile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
        default='pending'
    )

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"Appointment: {self.owner} ↔ {self.sitter} on {self.date}"