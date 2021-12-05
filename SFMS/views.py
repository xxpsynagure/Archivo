from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(response):
    return HttpResponse('<h1>Student File Management System<h1>')

def StudentLogin(response):
    return render (response, "StudentLogin.html")

def notfound(response):
    return render(response, "404.html")