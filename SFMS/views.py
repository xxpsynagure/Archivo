from django.shortcuts import render
from django.http import HttpResponse
from .models import students

from SFMS import models

# Create your views here.
def index(response):
    return HttpResponse('<h1>Student File Management System<h1>')

def StudentLogin(request):
    print('Hello workd')
    return render (request, "StudentLogin.html")

def StudentReg(request):
    return render(request, "StudentReg.html")

def notfound(request):
    print('Hello world')
    return render(request, "404.html")

def disp(request):
    #d1 = students.objects.all()
    # d1 = {'name': name, 'email':email}
    #return HttpResponse("Hi logged in", {'d1':d1})
    return HttpResponse('<h1>Successfully logged in </h1>')