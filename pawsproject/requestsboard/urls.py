
from django.urls import path
from . import views
app_name = 'requestsboard'
urlpatterns = [
    path('', views.list_requests, name='list'),
    path('new/', views.create_request, name='create'),
    path('mine/', views.my_requests, name='mine'),
    path('<int:pk>/edit/', views.update_request, name='update'),
    path('<int:pk>/delete/', views.delete_request, name='delete'),
]
