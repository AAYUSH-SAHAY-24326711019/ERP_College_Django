from django import forms
from appStudent.models import Student
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

    

    # def save(self, commit=True):
    #     student = super().save(commit=False)

    #     # create auth_user object
    #     user = User.objects.create_user(
    #         username=student.student_id,
    #         password=student.student_id
    #     )

    #     # link user
    #     student.user = user

    #     if commit:
    #         student.save()

    #     return student
    