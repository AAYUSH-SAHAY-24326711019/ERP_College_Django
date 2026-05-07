from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import Faculty,ActivityLogsFaculty

# Create your views here.
def faculty_login(request):

    if request.method=="POST":
        faculty_id = request.POST.get("faculty_id")
        password = request.POST.get("password")

        try:
            faculty = Faculty.objects.get(faculty_id=faculty_id)

            #temp pwd check

            if password == faculty.faculty_id:
                #store into logs of activity
                ActivityLogsFaculty.objects.create(
                    faculty=faculty,
                    action='Login'
                )

                return render(request, 
                    'faculty_module/faculty_dashboard.html',{
                        'faculty':faculty
                    }
                            )
            else:
                return render(request, 
                    'faculty_module/login.html',{
                        'error':'Invalid Password'
                    }
                            )
            
        except Faculty.DoesNotExist:
            return render(request,
                          'faculty_module/login.html',
                          {
                              "error":'faculty id invalid'
                          }
                          )   


    return render(request, "faculty_module/login.html")


def faculty_logout(request):

    if request.method=="POST":
        faculty_id=request.POST.get('faculty_id')
        try:
            faculty = Faculty.objects.get(
                faculty_id=faculty_id
            )
            #store logout activity

            ActivityLogsFaculty.objects.create(
                faculty=faculty,
                action='Logout'
            )
        except Faculty.DoesNotExist:
            pass

    return redirect('faculty_login')