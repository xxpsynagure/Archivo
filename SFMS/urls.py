from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("StudentLogin/", views.StudentLogin, name="StudentLogin"),
    path("StudentReg/",views.StudentReg, name="StudentReg"),
    #path("404/", views.notfound, name="ERROR404"),
    path("doLogin",views.doLogin, name="doLogin"),
    path("doReg",views.doReg,name="doReg"),
    path("trial",views.trial),
]

