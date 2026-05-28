from django.contrib.auth.models import User
from appStudent.models import Student
from appFaculty.models import Faculty

print("Initiate user_creation for all records [student]")
students = Student.objects.all()
for student in students:
  user_exists = User.objects.filter(username=student.student_id).exists() 
  if user_exists:
      continue
  user = User.objects.create_user(username=student.student_id,password=student.student_id)
  student.user = user
  student.save()
print("Done user_creation for all records [student]")

print("Initiate user_creation for all records [faculty]")
faculties = Faculty.objects.all()
for faculty in faculties:
    user_exists = User.objects.filter(username=faculty.faculty_id).exists()
    if user_exists:
        continue
    user=User.objects.create_user(username=faculty.faculty_id,password=faculty.faculty_id)
    faculty.user = user
    faculty.save()
print("Done user_creation for all records [faculty]")