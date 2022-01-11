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
    path("StudentDashboard",views.StudentDashboard,name="StudentDashboard"),
    path("TeacherDashboard",views.TeacherDashboard, name="TeacherDashboard"),
    path("StudentDashboard/StudentProfile", views.StudentProfile, name="StudentProfile"),
    path("TeacherDashboard/TeacherProfile", views.TeacherProfile, name="TeacherProfile"),
    path("StudentDashboard/<SubjectCode>", views.StudentFilePage, name="StudentFilePage"),
    path("notifications",views.notifications, name="notifications"),
]

