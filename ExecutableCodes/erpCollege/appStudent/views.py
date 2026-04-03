from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# Create your views here.
def myfunctioncall(request):
    return HttpResponse("Hello World")
    # return render(request, "login_student/index.html")

def logstudent(request):
    return render(request, "login_student/index.html")

def loghod(request):
    return render(request, "login_HOD/index.html")
