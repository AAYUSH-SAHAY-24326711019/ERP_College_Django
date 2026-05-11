from django.db import models
from appErpAdmin.models import CourseSessions

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=25)
    student_id = models.CharField(max_length=12,unique=True)
    course = models.CharField(max_length=6)
    email = models.EmailField(unique=True)
    session= models.CharField(max_length=10)
    image=models.ImageField(upload_to='students/')
    date_created = models.DateTimeField(auto_now_add=True)

    
class ActivityLogs(models.Model):

    ACTION_CHOICES = [
        ('Login', 'Login'),
        ('Logout', 'Logout'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.student_id} - {self.action}"
 
