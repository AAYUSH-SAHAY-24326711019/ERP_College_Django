import json
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from .models import ErpAdmin
from appMainsite.models import MainsiteEnquiryForm
from appStudent.models import Student
from appErpAdmin.models import Courses,University,CourseSessions,StudentEnrollment
import csv
import calendar
from datetime import datetime
from django.utils.timezone import now






# Create your views here.



def admin_login(request):
    

    # =========================
    # LOGIN PROCESS
    # =========================

    if request.method == "POST":

        admin_email = request.POST.get('admin_email')

        password = request.POST.get('password')

        try:

            admin = ErpAdmin.objects.get(
                email=admin_email,
                password=password
            )

            # SESSION
            request.session['admin_id'] = admin.id
            request.session['admin_name'] = admin.name
            request.session['admin_role'] = admin.role.role

            # =========================
            # DASHBOARD DATA
            # =========================

            current_date = datetime.now()

            year = current_date.year

            month = current_date.month

            enquiries = MainsiteEnquiryForm.objects.filter(
                created_at__year=year,
                created_at__month=month
            ).order_by('-id')

            months = []

            for i in range(1, 13):

                months.append({
                    'number': i,
                    'name': calendar.month_name[i]
                })

            courses = Courses.objects.all()
            universities = University.objects.all()
            current_courses = CourseSessions.objects.all()
            
            context = {

                'enquiries': enquiries,

                'months': months,

                'current_month': month,

                'current_year': year,

                'courses': courses,

                'universities': universities,

                'current_courses':current_courses,

            }

            return render(
                request,
                'erpadmin/dashboard.html',
                context
            )

        except ErpAdmin.DoesNotExist:

            return render(
                request,
                'erpadmin/index.html',
                {
                    'error': 'Invalid Credentials'
                }
            )



    # =========================
    # IF NOT LOGGED IN
    # =========================

    if 'admin_id' not in request.session:

        return render(
            request,
            'erpadmin/index.html'
        )



    # =========================
    # DASHBOARD FILTERING
    # =========================

    current_date = datetime.now()

    year = int(
        request.GET.get(
            'year',
            current_date.year
        )
    )

    month = int(
        request.GET.get(
            'month',
            current_date.month
        )
    )

    enquiries = MainsiteEnquiryForm.objects.filter(
        created_at__year=year,
        created_at__month=month
    ).order_by('-id')

    months = []

    for i in range(1, 13):

        months.append({
            'number': i,
            'name': calendar.month_name[i]
        })

    courses = Courses.objects.all()
    universities = University.objects.all()
    context = {

        'enquiries': enquiries,

        'months': months,

        'current_month': month,

        'current_year': year,

        'courses': courses,

        'universities': universities,

    }

    if request.GET.get('ajax'):

        return render(
            request,
            'erpadmin/partials/mainsite_enquiry_rows.html',
            context
        )

    return render(
        request,
        'erpadmin/dashboard.html',
        context
    )



# ==========================================
# CSV DOWNLOAD VIEW
# ==========================================

def download_mainsite_csv(request):

    if 'admin_id' not in request.session:

        return redirect('admin_login')

    current_date = datetime.now()

    year = int(
        request.GET.get(
            'year',
            current_date.year
        )
    )

    month = int(
        request.GET.get(
            'month',
            current_date.month
        )
    )

    enquiries = MainsiteEnquiryForm.objects.filter(
        created_at__year=year,
        created_at__month=month
    ).order_by('-id')

    response = HttpResponse(content_type='text/csv')

    filename = f"mainsite_enquiries_{month}_{year}.csv"

    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)

    writer.writerow([
        'Name',
        'Mobile',
        'From Place',
        'Course',
        'Created At'
    ])

    for enquiry in enquiries:

        writer.writerow([
            enquiry.name,
            enquiry.mobile,
            enquiry.from_place,
            enquiry.course,
            enquiry.created_at
        ])

    return response


def admin_logout(request):

    request.session.flush()

    return redirect('admin_login')

def course_session_page(request):

    courses = CourseSessions.objects.all()
    universities = University.objects.all()

    sessions = CourseSessions.objects.select_related(
        'course', 'university'
    ).all()

    return render(request, 'course_session.html', {
        'courses': courses,
        'universities': universities,
        'sessions':sessions,
    })

def save_course_session(request):

    if request.method == "POST":

        course_id = request.POST.get('course')
        university_id = request.POST.get('university')
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')

        course = Courses.objects.get(id=course_id)
        university = University.objects.get(id=university_id)

        obj = CourseSessions.objects.create(
            course=course,
            university=university,
            start_year=start_year,
            end_year=end_year
        )

        data = {
            'id': obj.id,
            'complete_name': obj.complete_name
        }

        return JsonResponse(data)

    return JsonResponse({'error': 'Invalid Request'})


from .models import CourseSessions

def showRecords(request):
    records = CourseSessions.objects.all()

    return render(request,'erpadmin/student_enrollment.html',
                  {'records':records})


# def seeCurrentCourses(request):
    

def showStudentCourse(request):

    if request.method =="POST":
        studentid = request.POST.get("student_id")
        id_list = [int(x.strip()) for x in studentid.split(",")]
        courseid = request.POST.get("course_id")

        for i in id_list:
            x=courseid
            student_obj = Student.objects.get(id=i)
            course_obj = CourseSessions.objects.get(id=x)
            StudentEnrollment.objects.create(student=student_obj,course=course_obj)
        
        data=StudentEnrollment.objects.all()
        context1={
            'data':data
        }

        return render(request, 'erpadmin/success.html',context1)

    return redirect('dashboard')



