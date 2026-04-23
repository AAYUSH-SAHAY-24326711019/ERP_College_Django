from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.admin_home, name='admin_home'),
    path('', views.admin_login, name='admin_login'),
]