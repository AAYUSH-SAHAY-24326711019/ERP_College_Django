from django.shortcuts import render,redirect
from .models import ErpAdmin
from appMainsite.models import MainsiteEnquiryForm
import csv
import calendar
from datetime import datetime
from django.http import HttpResponse,JsonResponse
from .models import Courses,University,CourseSessions

from appStudent.models import Student,StudentCourseEnrollment

import json
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

            context = {

                'enquiries': enquiries,

                'months': months,

                'current_month': month,

                'current_year': year,

                'courses': courses,

                'universities': universities

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

    return render(request, 'course_session.html', {
        'courses': courses,
        'universities': universities
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

def add_students_to_course(request):

    if request.method == "POST":

        data = json.loads(request.body)

        student_ids = data.get("student_ids")
        course_id = data.get("course_id")

        ids = [x.strip() for x in student_ids.split(",")]

        course = CourseSessions.objects.filter(id=course_id).first()

        if not course:
            return JsonResponse({
              "status": "error",
           "message": f"CourseSession with id {course_id} not found"
            })

        added = 0

        for sid in ids:

            try:

                student = Student.objects.get(student_id=sid)

                StudentCourseEnrollment.objects.get_or_create(
                student=student,
                course_session=course
                )

                added += 1

            except:
                pass


        print("COURSE ID RECEIVED:", course_id)
        print(CourseSessions.objects.all().values())
        return JsonResponse({
            "status": "success",
            "message": f"{added} students added successfully"
        })



def course_students_ajax(request, course_id):

    course = CourseSessions.objects.filter(id=course_id).first()

    if not course:
        return JsonResponse({
            "students": []
        })

    students = StudentCourseEnrollment.objects.filter(
        course_session=course
    )

    data = []

    for item in students:

        data.append({
            "student_id": item.student.student_id,
            "name": item.student.name,
            "course": item.course_session.complete_name
        })

    return JsonResponse({
        "students": data
    })