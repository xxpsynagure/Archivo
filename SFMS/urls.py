from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("Login/", views.Login, name="Login"),
    path("StudentReg/",views.StudentReg, name="StudentReg"),
    path("TeacherReg/",views.TeacherReg, name="TeacherReg"),
    #path("404/", views.notfound, name="ERROR404"),
    path("doLogin",views.doLogin, name="doLogin"),
    path("doReg",views.doReg,name="doReg"),
    path("trial",views.trial),
    path("rough",views.rough,name="try"),
]

