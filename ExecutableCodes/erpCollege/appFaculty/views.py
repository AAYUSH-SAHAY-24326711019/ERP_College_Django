from django.shortcuts import render

# Create your views here.
def logfaculty(request):
    return render(request, "login_faculty/index.html")