from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import Student, ActivityLogs


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
