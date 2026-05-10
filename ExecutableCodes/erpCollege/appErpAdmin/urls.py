from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('download-mainsite-csv/',views.download_mainsite_csv,name='download_mainsite_csv'),
    path('logout/',views.admin_logout,name='admin_logout'),

]