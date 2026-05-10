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
    

class Courses(models.Model):
    id = models.AutoField(primary_key=True)

    COURSE_CHOICES = [
        ('BCA', 'BCA'),
        ('BSC IT', 'BSC IT'),
        ('BBA', 'BBA'),
        ('BCOM', 'BCOM'),
        ('PGDM', 'PGDM'),
        ('MBA', 'MBA'),
        ('MCA', 'MCA'),
    ]

    course_name = models.CharField(
        max_length=100,
        choices=COURSE_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.course_name


class University(models.Model):
    id = models.AutoField(primary_key=True)

    UNIVERSITY_CHOICES = [
        ('AKU', 'AKU'),
        ('PPU', 'PPU'),
    ]

    university_name = models.CharField(
        max_length=100,
        choices=UNIVERSITY_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.university_name

class CourseSessions(models.Model):
    id = models.AutoField(primary_key=True)

    course = models.ForeignKey(
        Courses,
        on_delete=models.CASCADE
    )

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE
    )

    start_year = models.IntegerField()

    end_year = models.IntegerField()

    complete_name = models.CharField(
        max_length=255,
        unique=True
    )

    def save(self, *args, **kwargs):
        self.complete_name = f"{self.course.course_name}_{self.university.university_name}_{self.start_year}-{self.end_year}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.complete_name