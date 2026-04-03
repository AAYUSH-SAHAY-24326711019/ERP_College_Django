from django.shortcuts import render

# Create your views here.
def loghod(request):
    return render(request, "login_HOD/index.html")
