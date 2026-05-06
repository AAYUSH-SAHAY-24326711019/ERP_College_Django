from django.shortcuts import render,redirect
from .models import MainsiteEnquiryForm

# Create your views here.
# Create your views here.
def mainsite(request):
    return render(request,"MainSite/mainsite.html")

def mainsite(request):
    if request.method =="POST":
        MainsiteEnquiryForm.objects.create(
            name=request.POST.get("name"),
            mobile=request.POST.get("mobile"),
            from_place=request.POST.get("from_place"),
            course=request.POST.get("course",)
        )
        return redirect("index")
    
    return render(request,"MainSite/mainsite.html")



