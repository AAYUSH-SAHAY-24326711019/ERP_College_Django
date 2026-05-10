from django.shortcuts import render,redirect
from .models import ErpAdmin


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
        
    return render(request,'erpadmin/index.html')
        



