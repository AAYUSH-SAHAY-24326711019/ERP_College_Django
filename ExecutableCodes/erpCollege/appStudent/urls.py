from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),
    path(
        'upload-image/',
        views.upload_student_image,
        name='upload_student_image'
    ),
]