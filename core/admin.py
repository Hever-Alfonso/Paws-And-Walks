from django.contrib import admin
from .models import Sitter, ServiceRequest

@admin.register(Sitter)
class SitterAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_hour', 'is_verified')
    search_fields = ('name',)

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('owner_name', 'pet_name', 'service_type', 'sitter', 'created_at')
    list_filter = ('service_type', 'created_at')
    search_fields = ('owner_name', 'pet_name')