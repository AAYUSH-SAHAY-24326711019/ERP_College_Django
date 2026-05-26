from django import forms
from appStudent.models import Student
from appFaculty.models import Faculty
from django.contrib.auth.models import User

class Form1_main(forms.ModelForm):
    class Meta:
        model = Student

        fields =[
            "id",
            "name", 
            "student_id", 
            "course", 
            "email", 
            "session",
          
        ]
        def save(self, commit=True):
            student = super().save(commit=False)

            # create user only if not linked already
            if not student.user:
                user, created = User.objects.get_or_create(
                username=student.student_id
                )

                if created:
                    user.set_password(student.student_id)
                    user.save()

            student.user = user

            if commit:
                student.save()

            return student

class Form2_main(forms.ModelForm):
    class Meta:
        model = Faculty

        fields =[
            "faculty_id",
            "faculty_name",
            "faculty_email",
            "optionselected",
            "faculty_designation",
          
        ]
        def save(self, commit=True):
            faculty = super().save(commit=False)

            # create user only if not linked already
            if not faculty.user:
                user, created = User.objects.get_or_create(
                username=faculty.faculty_id
                )

                if created:
                    user.set_password(faculty.faculty_id)
                    user.save()

            faculty.user = user

            if commit:
                faculty.save()

            return faculty