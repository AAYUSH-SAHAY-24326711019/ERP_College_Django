from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import Faculty,ActivityLogsFaculty,FacultyAssignedSubject
from appErpAdmin.models import Courses,University,CourseSessions,StudentEnrollment
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
from .models import FacultyWiseAttendance
from .models import StudentWiseAttendance


# Create your views here.
def faculty_login(request):

    course_session_it = CourseSessions.objects.filter(

        Q(complete_name__startswith='BCA') |
        Q(complete_name__startswith='BSC') |
        Q(complete_name__startswith='MCA') 
    )
    course_session_manag = CourseSessions.objects.filter(

        Q(complete_name__startswith='BBA') |
        Q(complete_name__startswith='BCOM') |
        Q(complete_name__startswith='MBA') |
        Q(complete_name__startswith='PGDM') 
    )


    if request.method=="POST":
        faculty_id = request.POST.get("faculty_id")
        password = request.POST.get("password")
        
        try:
            faculty = Faculty.objects.get(faculty_id=faculty_id)

            #temp pwd check

            # jwt code

            user = authenticate(
            username=faculty_id,
            password=password
            )

            # if password == faculty.faculty_id:
            if user is not None:
                # jwt code
                refresh = RefreshToken.for_user(faculty)
                access_token = str(refresh.access_token)
                # print(access_token)
                request.session['access_token'] = access_token
                
                # 

                token = request.session.get('access_token')
                #store into logs of activity
                if token:
                    jwt_auth = JWTAuthentication()
                    validated_token = jwt_auth.get_validated_token(token)
                    ActivityLogsFaculty.objects.create(
                        faculty=faculty,
                        action='Login'
                    )
                    # print(faculty.faculty_id)
                    request.session['f_id']=faculty.faculty_id
                    return render(request, 
                        'faculty_module/faculty_dashboard.html',{
                            'faculty':faculty,
                            'course_session_it':course_session_it,
                            'course_session_manag':course_session_manag,
                            'fid':faculty.faculty_id,
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

# --
def mark_attendance(request):

    faculty_id = request.session.get('f_id')
    # faculty = Faculty.objects.get(
    #     faculty_id='fa010'
    # )
# point of error
    faculty = Faculty.objects.get(
        faculty_id=faculty_id
    )

    assigned_subjects = FacultyAssignedSubject.objects.filter(
        faculty=faculty.faculty_id
    )

    courses = CourseSessions.objects.all()

    if request.method == 'POST':

        subject = request.POST.get('subject')

        course_id = request.POST.get('course')

        present_students = request.POST.get(
            'present_students'
        )

        course = CourseSessions.objects.get(
            id=course_id
        )

        FacultyWiseAttendance.objects.create(

            attendance_date=datetime.now(),

            course_name=course.complete_name,

            faculty_id=faculty.faculty_id,

            faculty_name=faculty.faculty_name,

            subject=subject,

            attendance=present_students
        )

        if present_students:

            present_students_list = present_students.split(',')

            for student_id in present_students_list:

                StudentWiseAttendance.objects.create(

                    attendance_date=datetime.now(),

                    course_name=course.complete_name,

                    subject=subject,

                    faculty_id=faculty.faculty_id,

                    student_id=student_id
                )

    context = {
        'faculty': faculty,
        'subjects': assigned_subjects,
        'courses': courses,
        'current_datetime': datetime.now()
    }

    return render(
        request,
        'faculty_module/mark_attendance.html',
        context
    )

def get_students_by_course(request):

    course_id = request.GET.get('course_id')

    enrollments = StudentEnrollment.objects.filter(
        course_id=course_id
    )

    student_data = []

    for enrollment in enrollments:

        student = enrollment.student

        student_data.append({
            'id': student.id,
            'student_id': student.student_id,
            'name': student.name
        })

    return JsonResponse(student_data, safe=False)
# --