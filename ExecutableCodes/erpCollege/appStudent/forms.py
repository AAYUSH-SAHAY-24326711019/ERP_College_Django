from django import forms
from .models import Student

class StudentImageUploadForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['image']