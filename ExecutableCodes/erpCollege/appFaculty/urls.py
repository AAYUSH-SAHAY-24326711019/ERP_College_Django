from django.urls import path
from .import views


urlpatterns = [
    path('', views.faculty_login, name='faculty_login'),
    path('logout/', views.faculty_logout, name='faculty_logout'),
    path('makeSchedulesIT/',views.makeSchedulesIT,name='makeSchedulesIT'),
    path('makeSchedulesM/',views.makeSchedulesM,name='makeSchedulesM'),
    path('add-faculty-subject/',views.add_faculty_subject,name='add_faculty_subject'),
]