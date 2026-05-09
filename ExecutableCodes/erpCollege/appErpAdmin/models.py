from django.db import models

# Create your models here.

class AdminRoles(models.Model):
    role_id = models.AutoField(primary_key=True)

    role = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.role
    
class ErpAdmin(models.Model):
    id=models.AutoField(primary_key=True)

    role = models.ForeignKey(
        AdminRoles,
        on_delete=models.CASCADE,
        db_column='role_id'
    )

    name = models.CharField(max_length=150)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name