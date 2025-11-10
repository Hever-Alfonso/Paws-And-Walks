from django.contrib import admin
from .models import SitterProfile, SitterService, SitterRating, Message, Appointment

@admin.register(SitterService)
class SitterServiceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'get_service_type_display', 'price_cop')
    list_filter = ('service_type',)
    search_fields = ('profile__user__username',)

admin.site.register(SitterProfile)
admin.site.register(SitterRating)
admin.site.register(Message)
admin.site.register(Appointment)