from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import Student, ActivityLogs
from .forms import StudentImageUploadForm


def student_login(request):
    if request.method=="POST":
        student_id = request.POST.get("student_id")
        password = request.POST.get("password")

        try:
            student = Student.objects.get(student_id=student_id)

            #temp pwd check

            if password == student.student_id:
                #store into logs of activity
                ActivityLogs.objects.create(
                    student=student,
                    action='Login'
                )

                return render(request, 
                    'student_module/student_dashboard.html',{
                        'student':student
                    }
                            )
            else:
                return render(request, 
                    'student_module/login.html',{
                        'error':'Invalid Password'
                    }
                            )
            
        except Student.DoesNotExist:
            return render(request,
                          'student_module/login.html',
                          {
                              "error":'Student id invalid'
                          }
                          )



    return render(request, 'student_module/login.html')

def student_logout(request):

    if request.method=="POST":
        student_id=request.POST.get('student_id')
        try:
            student = Student.objects.get(
                student_id=student_id
            )
            #store logout activity

            ActivityLogs.objects.create(
                student=student,
                action='Logout'
            )
        except Student.DoesNotExist:
            pass

    return redirect('student_login')

def upload_student_image(request):

    if request.method == 'POST':

        student_id = request.POST.get('student_id')

        try:
            student = Student.objects.get(student_id=student_id)

        except Student.DoesNotExist:
            return render(
                request,
                'student_module/login.html',
                {
                    'error': 'Student id invalid'
                }
            )

        form = StudentImageUploadForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():
            form.save()

            return render(
                request,
                'student_module/student_dashboard.html',
                {
                    'student': student,
                    'success': 'Image uploaded successfully'
                }
            )

    return redirect('student_login')

    if request.method == 'POST':

        student_id = request.POST.get('student_id')

        try:
            student = Student.objects.get(student_id=student_id)

        except Student.DoesNotExist:
            return render(request,
                'student_module/upload_image.html',
                {
                    'error': 'Student ID invalid'
                }
            )

        form = StudentImageUploadForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():
            form.save()

            return render(request,
                'student_module/student_dashboard.html',
                {
                    'student': student
                }
            )

    return render(request, 'student_module/upload_image.html')
