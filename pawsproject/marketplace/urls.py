# marketplace/urls.py
from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    # Página principal
    path('', views.home, name='home'),

    # Gestión del perfil del cuidador
    path('me/profile/', views.my_profile, name='my_profile'),
    path('me/services/', views.my_services, name='my_services'),
    path('me/services/<int:pk>/delete/', views.delete_service, name='delete_service'),
    path('profile/delete/', views.delete_my_profile, name='delete_my_profile'),

    # Perfil público y funcionalidades protegidas
    path('sitter/<int:pk>/', views.sitter_detail, name='sitter_detail'),

    # Calificaciones
    path('sitter/<int:pk>/rate/', views.rate_sitter, name='rate_sitter'),
    path('sitter/<int:pk>/rate/edit/', views.edit_rating, name='edit_rating'),
    path('sitter/<int:pk>/rate/delete/', views.delete_rating, name='delete_rating'),

    # Chat (AJAX)
    path('sitter/<int:pk>/send-message/', views.send_message_ajax, name='send_message'),
]