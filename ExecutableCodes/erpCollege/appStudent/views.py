from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import Student, ActivityLogs
from .forms import StudentImageUploadForm
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from appFaculty.models import Faculty, StudentWiseAttendance
from appFaculty.models import FacultyWiseAttendance
from django.db.models import Count

def student_login(request):
    if request.method=="POST":
        student_id = request.POST.get("student_id")
        password = request.POST.get("password")

        try:
            student = Student.objects.get(student_id=student_id)

            #temp pwd check
# -------------------------------------------------------------------
            user = authenticate(
            username=student_id,
            password=password
            )
            # if password == student.student_id:
            if user is not None:
                # jwt code
                refresh = RefreshToken.for_user(student)
                access_token = str(refresh.access_token)
                # print(access_token)
                request.session['access_token'] = access_token
                request.session['s_id']=student_id
                print(student_id)
                # 

                token = request.session.get('access_token')
                if token:
                    jwt_auth = JWTAuthentication()
                    validated_token = jwt_auth.get_validated_token(token)
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
# -------------------------------------------------------------------
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


def student_attendance_dashboard(request):

    student_id = request.session.get(
        's_id'
    )

    attendance_logs = StudentWiseAttendance.objects.filter(
        student_id=student_id
    ).order_by('-attendance_date')

    # faculty_map = {
    # f.faculty_id: f.faculty_name
    # for f in Faculty.objects.all()
    # }
    faculty_map = {
    f.faculty_id: {
        'name': f.faculty_name,
        'designation': f.faculty_designation
    }
    for f in Faculty.objects.all()
    }

    # for log in attendance_logs:
    #     log.faculty_name = faculty_map.get(log.faculty_id, "Unknown")

    for log in attendance_logs:
        faculty = faculty_map.get(log.faculty_id)

        if faculty:
            log.faculty_display = (
            f"{faculty['name']} ({faculty['designation']})"
            )
        else:
            log.faculty_display = "Unknown"

    attendance_summary = []

    subjects = StudentWiseAttendance.objects.filter(
        student_id=student_id
    ).values(
        'subject'
    ).distinct()

    for sub in subjects:

        subject_name = sub['subject']

        total_classes = FacultyWiseAttendance.objects.filter(
            subject=subject_name
        ).count()

        present_classes = StudentWiseAttendance.objects.filter(
            student_id=student_id,
            subject=subject_name
        ).count()

        percentage = 0

        if total_classes > 0:

            percentage = (
                present_classes / total_classes
            ) * 100

        attendance_summary.append({

            'subject': subject_name,

            'total_classes': total_classes,

            'present_classes': present_classes,

            'percentage': round(percentage, 2)

        })
    
    context = {

    'attendance_logs': attendance_logs,

    'attendance_summary': attendance_summary,

    'student_id': student_id
    }

    return render(
        request,
        'student_module/student_attendance.html',
        context
    )
