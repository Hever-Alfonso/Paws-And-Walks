from django.urls import path
from . import views

urlpatterns = [
    path('', views.pet_assistant, name='pet_assistant'),
    path('reset/', views.pet_assistant_reset, name='pet_assistant_reset'),
]