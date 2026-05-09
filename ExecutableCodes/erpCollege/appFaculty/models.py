from django.db import models


class Faculty(models.Model):

    DESIGNATION_CHOICES = [
        ('Professor', 'Professor'),
        ('Guest Lecturer', 'Guest Lecturer'),
        ('Assistant Professor', 'Assistant Professor'),
        ('HOD - IT', 'HOD - IT'),
        ('HOD - Management', 'HOD - Management'),
        ('IT / Skill Trainer', 'IT / Skill Trainer'),
    ]

    date_created = models.DateTimeField(auto_now_add=True)

    faculty_email = models.EmailField(unique=True)

    faculty_name = models.CharField(max_length=100)

    faculty_id = models.CharField(
        max_length=4,
        unique=True
    )

    faculty_designation = models.CharField(
        max_length=50,
        choices=DESIGNATION_CHOICES
    )

    optionselected = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.faculty_name} ({self.faculty_id})"


class ActivityLogsFaculty(models.Model):

    ACTION_CHOICES = [
        ('Login', 'Login'),
        ('Logout', 'Logout'),
    ]

    faculty = models.ForeignKey(
        Faculty,
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
        return f"{self.faculty.faculty_id} - {self.action}"
    

class FacultyAssignedSubject(models.Model):

    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        to_field='faculty_id',
        db_column='faculty_id',
        related_name='assigned_subjects'
    )

    subject_name = models.CharField(max_length=200)

    subject_code = models.CharField(max_length=20)

    semester = models.CharField(max_length=20)

    session = models.CharField(max_length=20)

    date_assigned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.faculty.faculty_name} - {self.subject_name}"