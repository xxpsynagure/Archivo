from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("StudentLogin/", views.StudentLogin, name="StudentLogin"),
    path("StudentReg/",views.StudentReg, name="StudentReg"),
    path("404/", views.notfound, name="ERROR404"),
]