from django.contrib import admin
from .models import FacultyWiseAttendance
from .models import StudentWiseAttendance
# Register your models here.

admin.site.register(FacultyWiseAttendance)
admin.site.register(StudentWiseAttendance)