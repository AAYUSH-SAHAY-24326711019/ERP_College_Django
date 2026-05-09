from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import Faculty,ActivityLogsFaculty,FacultyAssignedSubject

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



def makeSchedulesIT(request):

    faculties = Faculty.objects.filter(

        optionselected__in=[
            'opt1_IT_Only',
            'opt3_Both_roles'
        ]

    ).prefetch_related(
        'assigned_subjects'
    )

    context = {

        'faculties': faculties

    }

    return render(

        request,

        'faculty_module/schedulerIT.html',

        context

    )

def makeSchedulesM(request):
    
    faculties = Faculty.objects.filter(

        optionselected__in=[
            'opt2_Manag_Only',
            'opt3_Both_roles'
        ]

    ).prefetch_related(
        'assigned_subjects'
    )

    context = {

        'faculties': faculties

    }

    return render(

        request,

        'faculty_module/schedulerManagement.html',

        context

    )

def add_faculty_subject(request):

    if request.method == "POST":

        faculty_id = request.POST.get('faculty_id')

        subject_name = request.POST.get('subject_name')

        subject_code = request.POST.get('subject_code')

        semester = request.POST.get('semester')

        session = request.POST.get('session')

        try:

            faculty = Faculty.objects.get(
                faculty_id=faculty_id
            )

            FacultyAssignedSubject.objects.create(

                faculty=faculty,

                subject_name=subject_name,

                subject_code=subject_code,

                semester=semester,

                session=session

            )

        except Faculty.DoesNotExist:

            pass

    return redirect('makeSchedulesIT')