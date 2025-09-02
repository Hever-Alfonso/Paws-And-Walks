
from django.urls import path
from . import views
app_name = 'marketplace'
urlpatterns = [
    path('', views.home, name='home'),
    path('me/profile/', views.my_profile, name='my_profile'),
    path('me/services/', views.my_services, name='my_services'),
    path('<int:pk>/', views.sitter_detail, name='sitter_detail'),
    path('<int:pk>/rate/', views.rate_sitter, name='rate_sitter'),
    path('<int:pk>/rate/edit/', views.edit_rating, name='edit_rating'),
    path('<int:pk>/rate/delete/', views.delete_rating, name='delete_rating'),
]
