from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('post-login/', views.role_redirect, name='role_redirect'),
]
