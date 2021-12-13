from django.shortcuts import render
from django.http import HttpResponse

from SFMS import models

# Create your views here.
def index(response):
    return HttpResponse('<h1>Student File Management System<h1>')

def StudentLogin(request):
    return render (request, "StudentLogin.html")

def StudentReg(request):
    return render(request, "StudentReg.html")

#def notfound(request):
#    return render(request,'404.html')

def error_404(request,exception):
    return render(request, "404.html")



