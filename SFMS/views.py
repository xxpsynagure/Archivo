from django.db.models.fields import EmailField
from django.db.utils import DataError, DatabaseError, IntegrityError
from django.shortcuts import redirect, render
from django.http import HttpResponse, request, response
from django.contrib import messages
from SFMS import models
from django.db import connections
from django.core.exceptions import *

USN =''
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
            global USN
            USN=data[0][0]
            if(data[0][6]=='S'):
                print(USN)
                return redirect("StudentDashboard")
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
            T_or_S = 'T' if (request.META['HTTP_REFERER'][22:]) == 'TeacherReg/' else 'S'
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
            global USN
            USN = usn
            print(USN)
            if T_or_S == 'S':
                return redirect('StudentProfile')
            else:
                return redirect('TeacherProfile')
                
        else:
            messages.error(request, "Password not matching, Please Try again")
            return redirect(request.META['HTTP_REFERER'][22:])

def greeting():
    cur = connections['default'].cursor() 
    print(USN)
    cur.execute(f"CALL greetings('{USN}')")
    data = cur.fetchone()
    return data[0]

def trial(request): #trial purpose
    # posts = models.Registration.objects.all()
    # print(posts)
    # print(posts.query)

    # p=models.Registration.objects.raw('SELECT * FROM Registration')[0]
    # print(p.username,p.email)
    
    return render(request, "FilePage.html")

def StudentDashboard(request):
    cur = connections['default'].cursor()
    cur.execute(f"SELECT S.Subject_code, S.Subject_name FROM Subject S WHERE S.Class = (SELECT Class FROM Student WHERE usn = '{USN}')")
    data ={}
    for items in cur:
        data[items[0]] = items[1]
    print(data)
    return render(request, "StudentDashboard.html",{'username':greeting(), 'url':'/StudentDashboard', 'Purl':'/StudentDashboard/StudentProfile'}|{'subject':data})

def TeacherDashboard(request): 
    cur=connections['default'].cursor()
    cur.execute(f"SELECT C.Branch, C.Sem, C.Sec, S.Subject_code, S.Subject_name FROM Subject S, Class C WHERE ssid = '{USN}' AND S.Class = C.Class")
    
    data ={}
    for item in cur:
        name = item[0] + '-'+ str(item[1]) + '' + item[2]
        data[name]=item[4]
        
    print(data)
    return render(request, "TeacherDashboard.html",{'username':greeting(), 'url':'/TeacherDashboard', 'Purl':'/TeacherDashboard/TeacherProfile'}|{'subject':data})



def StudentProfile(request):
    if(request.method!='POST'):
        cur = connections['default'].cursor()
        cur.execute(f"SELECT S.*, C.Branch, C.Sem, C.Sec FROM Student S, Class C WHERE USN = '{USN}' and S.Class = C.Class")
        data = cur.fetchone()
        print(data)
        if data is None:
            cur = connections['default'].cursor()
            cur.execute(f"SELECT * FROM Registration WHERE usn_ssid = '{USN}'")
            data = cur.fetchone()
            return render(request, 'StudentProfile.html',{'username':greeting(), 'url':'/StudentDashboard', 'Purl':'/StudentDashboard/StudentProfile',
                                                        'usn':data[0], 'Fname':'', 'Lname':'', 'Branch':data[4], 'Sem':'', 'Sec':'',
                                                        'DOB':'', 'Email':data[2], 'Phno':'', 'Portfolio_links':'', 'About':''})
            
        return render(request, 'StudentProfile.html',{'username':greeting(), 'url':'/StudentDashboard', 'Purl':'/StudentDashboard/StudentProfile',
                                                        'usn':data[0], 'Fname':data[1], 'Lname':data[2], 'Branch':data[10], 'Sem':data[11], 'Sec':data[12],
                                                        'DOB':data[4], 'Email':data[5], 'Phno':data[6], 'Portfolio_links':data[8], 'About':data[9]})
    try:
        usn = request.POST.get("usn")
        Fname = request.POST.get("Fname")
        Lname = request.POST.get("Lname")
        Branch= request.POST.get("Branch")
        Sem = request.POST.get("Sem")
        Sec = request.POST.get("Sec")
        DOB = request.POST.get("DOB")
        Email = request.POST.get("Email")
        Phno = request.POST.get("Phno")
        Portfolio_links = request.POST.get("Portfolio_links")
        About = request.POST.get("About")
        Image = request.POST.get("Image")
        Class = Branch + str(Sem) + Sec
        print(Class)

    except ObjectDoesNotExist as e:
        print(e)
        messages.warning(request, "Form not filled, \n Please check again")
        return redirect('#')    
    
    print(usn, Fname, Lname, Branch, Sem, Sec, DOB, Email, Phno, Portfolio_links, About)

    try:
        cursor = connections['default'].cursor()
    except DatabaseError as e:
        print(e)
        messages.warning(request, "Cannot connect to Database \n Please try again later")
        return redirect('/#Error')
    try:
        cursor.execute(f"INSERT INTO Student VALUES('{usn}','{Fname}','{Lname}','{Class}','{DOB}', '{Email}', '{Phno}', '{Image}', '{Portfolio_links}', '{About}') ON DUPLICATE KEY UPDATE usn = '{usn}', Fname='{Fname}', Lname='{Lname}', Class='{Class}', DOB='{DOB}', Email='{Email}', Phno='{Phno}', Image='{Image}', Portfolio_links='{Portfolio_links}', About='{About}';")
    except IntegrityError as e:
        print(e)
        messages.error(request,e)
    messages.success(request, "Saved Succesfully")
    return redirect('StudentDashboard')

def TeacherProfile(request):
    if(request.method!='POST'):
        cur = connections['default'].cursor()
        cur.execute(f"SELECT * FROM Teacher WHERE SSID = '{USN}'")
        data = cur.fetchone()
        if data is None:
            cur = connections['default'].cursor()
            cur.execute(f"SELECT * FROM Registration WHERE usn_ssid = '{USN}'")
            data = cur.fetchone()
            return render(request, 'TeacherProfile.html',{'username':greeting(), 'url':'/TeacherDashboard', 'Purl':'/TeacherDashboard/TeacherProfile', 'ssid':data[0], 'Fname':'', 'Lname':'',
                                                        'Designation':'', 'Department':data[4], 'yr_of_exp':'', 'Email':data[2], 'Phno':'', 'Skills':''})

        return render(request, 'TeacherProfile.html',{'username':greeting(), 'url':'/TeacherDashboard', 'Purl':'/TeacherDashboard/TeacherProfile', 'ssid':data[0], 'Fname':data[1], 'Lname':data[2],
                                                        'Designation':data[3], 'Department':data[4], 'yr_of_exp':data[5], 'Email':data[6], 'Phno':data[7], 'Skills':data[8]})
    try:
        ssid = request.POST.get("ssid")
        Fname = request.POST.get("Fname")
        Lname = request.POST.get("Lname")
        Designation = request.POST.get("Designation")
        Department = request.POST.get("Department")
        yr_of_exp = request.POST.get("yr_of_exp")
        Email = request.POST.get("Email")
        Phno = request.POST.get("Phno")
        Skills = request.POST.get("Skills")
        Image = request.POST.get("Image")
    except ObjectDoesNotExist as e:
        print(e)
        messages.warning(request, "Form not filled, \n Please check again")
        return redirect('#')    
    
    print(ssid, Fname, Lname, Department, Designation, yr_of_exp, Email, Skills)

    try:
        cursor = connections['default'].cursor()
    except DatabaseError as e:
        print(e)
        messages.warning(request, "Cannot connect to Database \n Please try again later")
        return redirect('/#Error')
    try:
        cursor.execute(f"INSERT INTO Teacher VALUES('{ssid}','{Fname}','{Lname}','{Designation}','{Department}','{yr_of_exp}', '{Email}', '{Phno}', '{Skills}', '{Image}') ON DUPLICATE KEY UPDATE SSID='{ssid}', Fname='{Fname}', Lname='{Lname}', Designation='{Designation}', Department='{Department}', yr_of_exp='{yr_of_exp}', Email='{Email}', Phno='{Phno}',Skills='{Skills}', Image='{Image}';")
    except IntegrityError as e:
        print(e)
        messages.error(request, e.args)
    messages.success(request, "Saved sucessfully")
    return redirect('TeacherDashboard')


def StudentFilePage(request, SubjectCode):
    if request.method != "POST":
        cur = connections['default'].cursor()
        SubjectCode = str(SubjectCode)
        cur.execute(f"SELECT Reponame from Repository WHERE Subject_code = '{SubjectCode}' ;")
        data = {items[0]: items[0] for items in cur}
        print(data)
        cur.execute(f"SELECT Filename, Uploaded from File; ")
        filedata = {items[0]: items[1] for items in cur}
        return render(request, 'StudentFilePage.html', {'username':greeting(), 'SubjectName':SubjectCode, 'data':data, 'filedata':filedata})
    
    try:
        FileName = request.POST.get("FileName")
        File = request.POST.get("fileInput")
        RepoName = request.POST.get("RepoName")
    except ObjectDoesNotExist as e:
        print(e)
        messages.warning(request, "Form not filled, \n Please check again")
        return redirect('#')

    print(FileName.split('\\')[-1], RepoName, USN, type(File))
    FileName = FileName.split('\\')[-1]
    cur = connections['default'].cursor()
    cur.execute(f"""INSERT INTO File (Repoid, Filename, Usn, Content) VALUES 
                    ( (SELECT Repoid FROM Repository WHERE Reponame = '{RepoName}'), '{FileName}', '{USN}', '{File}')
                    """)

    return redirect('StudentFilePage', SubjectCode)