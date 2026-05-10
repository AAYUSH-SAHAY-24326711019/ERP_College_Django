from django.shortcuts import render,redirect
from .models import ErpAdmin
from appMainsite.models import MainsiteEnquiryForm
import csv
import calendar
from datetime import datetime
from django.http import HttpResponse


# Create your views here.



def admin_login(request):
    if request.method=="POST":
        admin_email = request.POST.get('admin_email')

        password = request.POST.get('password')

        try:
            admin = ErpAdmin.objects.get(
                email = admin_email,
                password=password
            )

            #session
            request.session['admin_id']=admin.id
            request.session['admin_name']=admin.name
            request.session['admin_role']=admin.role.role

            # return redirect('erp_dashboard')
            return render(request,'erpadmin/dashboard.html')
        
        except ErpAdmin.DoesNotExist:
            return render(request,'erpadmin/index.html',{'error':'Invalid Credentials'})
        
    # till here , below it all 
    # return render(request,'erpadmin/index.html')
        
    if 'admin_id' not in request.session:
        return render(request, 'erpadmin/index.html')

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

    return render(
        request,
        'erpadmin/dashboard.html',
        context
    )


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


