from django.db.models.fields import EmailField
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from SFMS import models
from django.db import connections

# Create your views here.
def index(request):
    return render(request,"index.html")

def Login(request):
    return render (request, "Login.html")

def StudentReg(request):
    cur = connections['default'].cursor()
    cur.execute(f"SELECT * FROM College ")
    params ={}
    for item in cur:
        params[item[0]]=item[1]
    print(params)
    print()
    cur.execute(f"SELECT * FROM Branch")
    branch = {}
    colli = []
    for item in cur:
        branch[item[0]] = item[1]
        colli.append(item[2])
    
    return render(request, 'StudentReg.html', {'params':params}|{'branch':branch}|{'colli':colli})

def TeacherReg(request):
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


def error_404(request,exception):
    return render(request, "404.html")

def doLogin(request):
    if(request.method!='POST'):
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
        user = request.POST.get("your_username")
        password = request.POST.get("your_pass")
        cur = connections['default'].cursor()
        p = models.Registration.objects.raw(f"SELECT * FROM Registration WHERE Username = '{user}' AND  Pass = md5('{password}');")

        if(p):
            messages.success(request, "Login successful")
            return HttpResponse("<h2>Login Successful</h2>")
        else:
            messages.error(request, "Username or Password not matching, Please try again")
            return redirect('Login')

def doReg(request):
    if(request.method!='POST'):
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
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

        if(passw==re_pass):
            cursor = connections['default'].cursor()
            cursor.execute(f"INSERT INTO Registration VALUES('{usn}','{user}','{email}',md5('{passw}'),'{branch}','{college}', '{T_or_S}');")
            return HttpResponse("<h2>Registration Successful</h2>")
        else:
            messages.error(request, "Password not matching, Please Try again")
            return redirect('TeacherReg')


def trial(request): #trial purpose
    posts = models.Registration.objects.all()
    print(posts)
    print(posts.query)

    p=models.Registration.objects.raw('SELECT * FROM Registration')[0]
    print(p.username,p.email)
    
    return HttpResponse("hello")
