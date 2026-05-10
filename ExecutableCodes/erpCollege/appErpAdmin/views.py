from django.shortcuts import render,redirect
from .models import ErpAdmin
from appMainsite.models import MainsiteEnquiryForm
import csv
import calendar
from datetime import datetime
from django.http import HttpResponse


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

            context = {

                'enquiries': enquiries,

                'months': months,

                'current_month': month,

                'current_year': year

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

    context = {

        'enquiries': enquiries,

        'months': months,

        'current_month': month,

        'current_year': year

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