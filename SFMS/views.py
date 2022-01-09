from django.db.models.fields import EmailField
from django.db.utils import DataError, DatabaseError, IntegrityError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from SFMS import models
from django.db import connections
from django.core.exceptions import *

# Create your views here.
def index(request):
    return render(request,"index.html")

def Login(request):
    return render (request, "Login.html")

def StudentReg(request):
    try:
        cur = connections['default'].cursor()
        cur.execute(f"SELECT * FROM College ")
        params ={}
        for item in cur:
            params[item[0]]=item[1]

        cur.execute(f"SELECT * FROM Branch")
        branch = {}
        colli = []
        for item in cur:
            branch[item[0]] = item[1]
            colli.append(item[2])
        
        return render(request, 'StudentReg.html', {'params':params}|{'branch':branch}|{'colli':colli})
    except DatabaseError or DataError as e:
        print(e.args)
        messages.warning(request, "Cannot connect to Database \n Please Try again later")
        return redirect('/#Error')

def TeacherReg(request):
    try:
        cur = connections['default'].cursor()
        cur.execute(f"SELECT * FROM College ")
        params ={}
        for item in cur:
            params[item[0]]=item[1]
        cur.execute(f"SELECT * FROM Branch")
        branch = {}
        colli = []
        for item in cur:
            branch[item[0]] = item[1]
            colli.append(item[2])
        
        return render(request, 'TeacherReg.html', {'params':params}|{'branch':branch}|{'colli':colli})
    except DatabaseError or DataError as e:
        print(e.args)
        messages.warning(request, "Cannot connect to Database \n Please try again later")
        return redirect('/#Error')


def error_404(request,exception):
    return render(request, "404.html")

def doLogin(request):
    if(request.method!='POST'):
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
        try:
            user = request.POST.get("your_username")
            password = request.POST.get("your_pass")
        except ObjectDoesNotExist as e:
            print(e)
            messages.warning(request, e.args)
            return redirect('Login')
        try:
            cur = connections['default'].cursor()
            p = cur.execute(f"SELECT * FROM Registration WHERE Username = '{user}' AND  Pass = md5('{password}');")
        except DatabaseError or DataError as e:
            print(e)
            messages.warning(request, "Cannot connect to Database, \n Please try again later")
            return redirect('Login')

        if(p):
            messages.success(request, "Login successful")
            data = cur.fetchall()
            if(data[0][6]=='S'):
                return redirect("/StudentDashboard")
            return redirect("TeacherDashboard")
        else:
            messages.error(request, "Username or Password not matching, Please try again")
            return redirect('Login')

def doReg(request):
    if(request.method!='POST'):
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
        try:
            user = request.POST.get("username")
            usn = request.POST.get("usn")
            email =request.POST.get("email")
            college =request.POST.get("college")
            branch =request.POST.get("branch")
            passw = request.POST.get("pass")
            re_pass =request.POST.get("re_pass")       
            if (request.META['HTTP_REFERER'][22:]) == 'TeacherReg/':
                T_or_S = 'T'
            else:
                T_or_S = 'S'
        except ObjectDoesNotExist as e:
            print(e)
            messages.warning(request, "Form not filled, \n Please check again")
            return redirect('/#Error')

        if(passw==re_pass):
            try:
                cursor = connections['default'].cursor()
            except DatabaseError as e:
                print(e)
                messages.warning(request, "Cannot connect to Database \n Please try again later")
                return redirect('/#Error')
            try:
                cursor.execute(f"INSERT INTO Registration VALUES('{usn}','{user}','{email}',md5('{passw}'),'{branch}','{college}', '{T_or_S}');")
            except IntegrityError as e:
                print(e)
                refer = {'PRIMARY':"USN/SSID already in use,\n Please Login", 'Username':"Username taken,\nPlease chose a new Username", 'Email':"Email taken, \nUse other Email","":"Please fill in details"}
                messages.warning(request, refer[str(e.args).split('.')[-1][:-3]])
                return redirect(request.META['HTTP_REFERER'][22:])

            messages.success(request, "Registration Succesful")
            return HttpResponse("<h2>Registration Successful</h2>")
        else:
            messages.error(request, "Password not matching, Please Try again")
            return redirect(request.META['HTTP_REFERER'][22:])



def trial(request): #trial purpose
    # posts = models.Registration.objects.all()
    # print(posts)
    # print(posts.query)

    # p=models.Registration.objects.raw('SELECT * FROM Registration')[0]
    # print(p.username,p.email)
    
    return render(request, "studentDetails.html")

def StudentDashboard(request): 
    return render(request, "StudentDashboard.html")

def TeacherDashboard(request): 
    return render(request, "TeacherDashboard.html")