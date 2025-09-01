from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sitters/', views.sitters_list, name='sitters_list'),
    path('request/', views.create_request, name='create_request'),
]