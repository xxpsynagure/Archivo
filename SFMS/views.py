from email.policy import default
from fileinput import filename
import mimetypes
import os
from webbrowser import Opera
from django.conf import settings
from django.db.models.fields import EmailField
from django.db.utils import DataError, DatabaseError, IntegrityError
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect, request, response
from django.contrib import messages
from SFMS import models
from django.db import OperationalError, connections
from django.core.exceptions import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import base64

USN =''
# Create your views here.
def index(request):
    return render(request,"index.html")

def Login(request):
    return render (request, "Login.html")

def StudentReg(request):
    try:
        cur = connections['default'].cursor()
        try:
            sql = "SELECT * FROM College"
            cur.execute(sql)
        except (IntegrityError,OperationalError) as e:
            print(e)
            messages.warning(request, 'Cannot fetch colleges')
        params ={}
        for item in cur:
            params[item[0]]=item[1]

        try:
            sql = "SELECT * FROM Branch"
            cur.execute(sql)
        except (IntegrityError,OperationalError) as e:
            print(e)
            messages.warning(request, "Cannot fetch branches")
        branch = {}
        colli = []
        for item in cur:
            branch[item[0]] = item[1]
            colli.append(item[2])
        
        return render(request, 'StudentReg.html', {'params':params}|{'branch':branch}|{'colli':colli})
    except DatabaseError or DataError as e:
        print(e.args)
        messages.warning(request, "Cannot connect to Database \n Please Try again later")
        raise Http404


def TeacherReg(request):
    try:
        cur = connections['default'].cursor()
        try:
            sql = "SELECT * FROM College"
            cur.execute(sql)
        except (IntegrityError,OperationalError) as e:
            print(e)
            messages.warning(request, "Cannot fetch colleges")
        params ={}
        for item in cur:
            params[item[0]]=item[1]
        try:
            sql = "SELECT * FROM Branch"
            cur.execute(sql)
        except (IntegrityError,OperationalError) as e:
            print(e)
            messages.warning(request, "Cannot fetch branches")
        branch = {}
        colli = []
        for item in cur:
            branch[item[0]] = item[1]
            colli.append(item[2])
        
        return render(request, 'TeacherReg.html', {'params':params}|{'branch':branch}|{'colli':colli})
    except DatabaseError or DataError as e:
        print(e.args)
        messages.warning(request, "Cannot connect to Database \n Please try again later")
        raise Http404

def error_404(request,exception):
    return render(request, "404.html")

def doLogin(request):
    if (request.method!='POST'):
        raise Http404
    
    try:   
        try:
            params = (request.POST.get("your_username"), request.POST.get("your_pass")) 
        except ObjectDoesNotExist as e:
            print(e)
            messages.warning(request, e.args)
            return redirect('Login')

        cur = connections['default'].cursor()
        sql = "SELECT * FROM Registration WHERE Username = %s AND  Pass = md5(%s);"
        p = cur.execute(sql, params)
    except (DatabaseError,DataError,IntegrityError) as e:
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
    if (request.method!='POST'):
        raise Http404
    try:
        usn = request.POST.get("usn")
        passw = request.POST.get("pass")
        re_pass = request.POST.get("re_pass")
        T_or_S = 'T' if (request.META['HTTP_REFERER'][22:]) == 'TeacherReg/' else 'S'

        params = ( usn,
                    request.POST.get("username"),
                    request.POST.get("email"),
                    passw,
                    request.POST.get("branch"),
                    request.POST.get("college"),
                    T_or_S)   
    except ObjectDoesNotExist as e:
        print(e)
        messages.warning(request, "Form not filled, \n Please check again")
        raise Http404

    if(passw==re_pass):
        try:
            cursor = connections['default'].cursor()
        except DatabaseError as e:
            print(e)
            messages.warning(request, "Cannot connect to Database \n Please try again later")
            return redirect('/#Error')
        try:
            sql = "INSERT INTO Registration VALUES(%s, %s, %s, md5(%s), %s, %s, %s);"   
            cursor.execute(sql, params)
        except IntegrityError or OperationalError as e:
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
    try:
        cur.execute("CALL greetings(%s)", (USN,))
    except (IntegrityError, OperationalError) as e:
        print(e)
        messages.warning(request, "Error in greeting , So exiting")
        return redirect('/')
    data = cur.fetchone()
    return data[0]

def trial(request): #trial purpose
    # posts = models.Registration.objects.all()
    # print(posts)
    # print(posts.query)

    # p=models.Registration.objects.raw('SELECT * FROM Registration')[0]
    # print(p.username,p.email)
    
    return render(request, "admin.html")

def StudentDashboard(request):
    try:
        cur = connections['default'].cursor()
    except DatabaseError as e:
        print(e)
        messages.warning(request, "Cannot connect to Database \n Please try again later")
        return redirect('Login')
    try:
        sql = """SELECT SH.Subject_code, S.Subject_name FROM Subject S, Subject_Handle SH 
                    WHERE S.Subject_code = SH.Subject_code 
                    AND SH.Class = (SELECT Class FROM Student WHERE usn = %s)"""
        cur.execute(sql, (USN,))
    except IntegrityError or OperationalError as e:
        print(e)
        messages.warning(request, "Internal error in fetching subjects")
        return redirect('Login')
    data = {items[0]: items[1] for items in cur}
    print(data)
    return render(request, "StudentDashboard.html",{'username':greeting(), 'url':'/StudentDashboard', 'Purl':'/StudentDashboard/StudentProfile'}|{'subject':data})


def TeacherDashboard(request): 
    cur=connections['default'].cursor()
    try:
        sql = """SELECT C.Branch, C.Sem, C.Sec, S.Subject_code, S.Subject_name 
                    FROM Subject S, Subject_Handle SH, Class C 
                    WHERE SH.ssid = %s AND SH.Class = C.Class AND SH.Subject_code = S.Subject_Code"""
        cur.execute(sql, (USN,))
    except (IntegrityError, OperationalError) as e:
        print(e)
        messages.warning(request, "Could not fetch Subjects")
    
    data ={}
    for item in cur:
        name = item[0] + '-'+ str(item[1]) + item[2]
        data[name]=item[4]
    print(data)

    if(request.method == 'POST'):
        try:
            Class = "".join(request.POST.get("class").split('-'))
            params = (USN, Class, request.POST.get("title"), request.POST.get("content"))

            cur=connections['default'].cursor()
            sql = "INSERT INTO Notification(ssid,Class,Title,Message) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, params)
            messages.success(request,"Message Sent")
            
        except (ObjectDoesNotExist,AttributeError,TypeError) as e:
            print(e)
            messages.warning(request, "Form not filled, \n Please check again")
            return redirect('TeacherDashboard')    
        
    return render(request, "TeacherDashboard.html",{'username':greeting(), 'url':'/TeacherDashboard', 'Purl':'/TeacherDashboard/TeacherProfile'}|{'subject':data})


def StudentProfile(request):
    if(request.method!='POST'):
        cur = connections['default'].cursor()
        try:
            sql = "SELECT S.*, C.Branch, C.Sem, C.Sec FROM Student S, Class C WHERE USN = %s and S.Class = C.Class"
            cur.execute(sql,(USN,))
        except (IntegrityError, OperationalError) as e:
            print(e)
            messages.error(request, "Cannot fetch the profile data from database")
        data = cur.fetchone()
        print(data)
        if data is None:
            cur = connections['default'].cursor()
            try:
                sql = "SELECT * FROM Registration WHERE usn_ssid = %s "
                cur.execute(sql, (USN,))
            except (IntegrityError, OperationalError) as e:
                print(e)
                messages.warning(request, "Cannot fetch profile data from Registration table of database")
            data = cur.fetchone()
            return render(request, 'StudentProfile.html',{'username':greeting(), 'url':'/StudentDashboard', 'Purl':'/StudentDashboard/StudentProfile',
                                                        'usn':data[0], 'Fname':'', 'Lname':'', 'Branch':data[4], 'Sem':'', 'Sec':'',
                                                        'DOB':'', 'Email':data[2], 'Phno':'', 'Portfolio_links':'', 'About':''})
            
        return render(request, 'StudentProfile.html',{'username':greeting(), 'url':'/StudentDashboard', 'Purl':'/StudentDashboard/StudentProfile',
                                                        'usn':data[0], 'Fname':data[1], 'Lname':data[2], 'Branch':data[10], 'Sem':data[11], 'Sec':data[12],
                                                        'DOB':str(data[4]), 'Email':data[5], 'Phno':data[6], 'Portfolio_links':data[8], 'About':data[9]})
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
    except (IntegrityError, OperationalError) as e:
        print(e)
        messages.error(request,e.args)
    messages.success(request, "Saved Succesfully")
    return redirect('StudentDashboard')

def TeacherProfile(request):
    if(request.method!='POST'):
        cur = connections['default'].cursor()
        try:
            cur.execute(f"SELECT * FROM Teacher WHERE SSID = '{USN}'")
        except (IntegrityError, OperationalError) as e:
            print(e)
            messages.error(request, e.args)
        data = cur.fetchone()
        if data is None:
            cur = connections['default'].cursor()
            try:
                cur.execute(f"SELECT * FROM Registration WHERE usn_ssid = '{USN}'")
            except (IntegrityError, OperationalError) as e:
                print(e)
                messages.error(request, e.args)
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
    except (IntegrityError,OperationalError) as e:
        print(e)
        messages.error(request, e.args)
    messages.success(request, "Saved sucessfully")
    return redirect('TeacherDashboard')


def StudentFilePage(request, SubjectCode):
    if request.method != "POST":
        if len(SubjectCode) > 7:
            raise Http404
        cur = connections['default'].cursor()
        SubjectCode = str(SubjectCode)
        try:
            cur.execute(f"SELECT Reponame from Repository WHERE Subject_code = '{SubjectCode}' and Class = (SELECT Class from Student WHERE USN = '{USN}') ;")
        except (IntegrityError, OperationalError) as e:
            print(e)
            messages.error(request, e.args)
        data = {items[0]: items[0] for items in cur}
        try:
            cur.execute(f"select f.filename, f.Uploaded,r.Reponame, f.Usn, f.Marks from file f ,Repository r where f.repoid in (select repoid from repository where subject_code = '{SubjectCode}') AND USN = '{USN}' AND f.Repoid = r.Repoid; ")
        except (IntegrityError, OperationalError) as e:
            print(e)
            messages.error(request, e.args)
        filedata = {items[0]: {'time':items[1], 'repo':items[2], 'by':items[3], 'marks':items[4]} for items in cur}
        print(filedata)
        return render(request, 'StudentFilePage.html', {'username':greeting(), 'SubjectName':SubjectCode, 'data':data, 'filedata':filedata, 'url':'/StudentDashboard', 'Purl':'/StudentDashboard/StudentProfile'})
    
    try:
        FileName = request.POST.get("FileName")
        File = request.FILES['fileInput']
        RepoName = request.POST.get("RepoName")
    except ObjectDoesNotExist as e:
        print(e)
        messages.warning(request, "Form not filled, \n Please check again")
        return redirect('#')

    print(FileName.split('\\')[-1], RepoName, USN, type(File))
    FileName = FileName.split('\\')[-1]
    FileLocation = USN+'/'+FileName
    path = default_storage.save(FileLocation, ContentFile(File.read())) # Downloading the file
    print(path)
    # print(File.content_type)
    # uploadFile = str(File.read())
    # # with open(uploadFile,"wb") as f:
    # #     f.replace("'","_")
    # # print(type(uploadFile))
    # uploadFile = uploadFile.replace("'","_")
    try:
        cur = connections['default'].cursor()
        cur.execute(f"""INSERT INTO File (Repoid, Filename, Usn, Location) VALUES 
                        ( (SELECT Repoid FROM Repository WHERE Reponame = '{RepoName}' AND Class = (SELECT Class FROM STUDENT WHERE USN = '{USN}') ), 
                        '{FileName}', '{USN}', '{FileLocation}')
                        """)
    except (IntegrityError,OperationalError) as e:
        print(e)
        messages.error(request, "Please select the Assignment repository before uploading the file")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # cur.execute(f"SELECT Filename,Content from file where Usn = '{USN}'")
    # file = cur.fetchone()

    return redirect('StudentFilePage', SubjectCode)

def TeacherFilePage(request, ClassName):
    if request.method != "POST":
        if len(ClassName) > 6:
            raise Http404
        cur = connections['default'].cursor()
        try:
            cur.execute(f"SELECT Reponame from Repository WHERE Class = '{ClassName.replace('-','')}' AND ssid = '{USN}' ;")
        except (IntegrityError, OperationalError) as e:
            print(e)
            messages.error(request, e.args)
        data = {items[0]: items[0] for items in cur}
        # print(data)
        try:
            cur.execute(f"""SELECT f.filename,f.Uploaded,r.Reponame,f.Usn,f.Marks 
                                FROM File f, Repository r WHERE f.repoid 
                                IN (SELECT rr.repoid FROM repository rr 
                                WHERE Class = '{ClassName.replace('-','')}' AND ssid = '{USN}') AND f.Repoid = r.Repoid; """)
        except (IntegrityError, OperationalError) as e:
            print(e)
            messages.error(request, e.args)
        filedata = {items[0]: {'time':items[1], 'repo':items[2], 'by':items[3], 'marks':items[4]} for items in cur}
        return render(request, "TeacherFilePage.html", {'username':greeting(), 'SubjectName':ClassName, 'data':data, 'filedata':filedata, 'url':'/TeacherDashboard', 'Purl':'/TeacherDashboard/TeacherProfile'})

    try:
        RepoName = request.POST.get('AssignmentName')
        #Repoid = request.POST.get('AssignmentID')
    except ObjectDoesNotExist as e:
        print(e)
        messages.warning(request, "Form not filled, \n Please check again")
        return redirect('#')
    ClassName = ClassName.replace('-','')
    print(RepoName, USN, ClassName, )
    cur = connections['default'].cursor()
    try:
        cur.execute(f"INSERT INTO Repository(Reponame, ssid, Class, Subject_code) VALUES ('{RepoName}', '{USN}', '{ClassName}', ( SELECT Subject_code FROM Subject_Handle WHERE ssid = '{USN}' and Class = '{ClassName}') )")
    except (IntegrityError, OperationalError) as e:
        print(e)
        messages.warning(request, "Assignment not created")
    finally:
        messages.success(request,"Assignment created")
    ClassName = ClassName[:3]+'-'+ClassName[3:]
    return redirect('TeacherFilePage', ClassName)

def notifications(request):
    cur = connections['default'].cursor()
    try:
        cur.execute(f"""SELECT DISTINCT M.* FROM Message_recieved M
                    WHERE M.Class = (SELECT S.Class FROM Student S WHERE S.usn = '{USN}')
                    ORDER BY M.Sent_time DESC;""")
    except (IntegrityError, OperationalError) as e:
        print(e)
        messages.warning(request, "Unable to update notification, please try again later.")
    #data = cur.fetchall()
    data=[]
    for tuple in cur.fetchall():
        dict = {}
        dict['name'] = tuple[1] + ' ' + tuple[2]
        dict['subject'] = tuple[3].capitalize()
        dict['sent_time'] = tuple[4]
        dict['title'] = tuple[5]
        dict['content'] = tuple[6]
        data.append(dict)
    # print(data)

    return render(request, "notifications.html",{'username':greeting()}|{'message':data,'url':'/StudentDashboard','Purl':'/StudentDashboard/StudentProfile'})


def downloadFile(request):
    if request.method == 'POST':
        # msg = json.loads(request.body)
        # print(msg)
        # return HttpResponse(json.dumps({'received':msg}))
        btn = request.POST.get('downloadButton')
        msg = request.POST.get('downloadValue')
        marks = request.POST.get("marks")
        print(btn, msg, marks)

        if btn is None:
            cur = connections['default'].cursor()
            cur.execute(f"UPDATE File SET Marks = {marks} WHERE USN = '{msg.split('/')[0]}' AND Filename = '{msg.split('/')[1]}' ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        # cur = connections['default'].cursor()
        # cur.execute(f"SELECT Content from file where Filename = '{msg}'")
        # data = cur.fetchone()
        # # print(data[0])
        # with open('tmp/'+msg, 'wb') as writefile:
        #     writefile.write(data[0])

        # with open('tmp/'+msg, 'r') as f:
        #     data = f.read()
        # with open('tmp/'+msg, "w") as wf:
        #     wf.write(data[2:-1].replace("_","'"))

        # redi = [items for items in request.META['HTTP_REFERER'][22:].split('/')]
        # print(redi)
        # messages.success(request, "File downloaded succesfully \n Please check in `/tmp` folder " )
        # return redirect(redi[0][:7]+'FilePage', redi[1])


        path = open(settings.MEDIA_ROOT+'/'+msg, 'rb')
    # Set the mime type
        mime_type, _ = mimetypes.guess_type(settings.MEDIA_ROOT+'/'+msg)
    # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % msg
    # Return the response value
        return response

def deleteFile(request):
    if request.method == 'POST':
        # msg = json.loads(request.body)
        # print(msg)
        # return HttpResponse(json.dumps({'received':msg}))
        msg = request.POST.get('deleteButton')
        msg = msg.split('/')

        cur = connections['default'].cursor()
        try:
            cur.execute(f"delete from file where Filename = '{msg[1]}' and Usn = '{msg[0]}'")
        except (IntegrityError, OperationalError) as e:
            print(e)
            messages.error(request, e.args)
        
        if os.path.isfile(settings.MEDIA_ROOT+'/'+'/'.join(msg)):
            os.remove(settings.MEDIA_ROOT+'/'+'/'.join(msg))

        messages.success(request, "File deleted succesfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def UserAdmin(request):
    if request.method != "POST":
        cur  = connections['default'].cursor()
        cur.execute(f"""SELECT Subject_Handle.*, Subject.Subject_name, Teacher.Fname, Teacher.Lname FROM Subject_Handle LEFT 
                        JOIN Teacher ON Subject_Handle.ssid = Teacher.ssid 
                        JOIN Subject ON Subject.Subject_code = Subject_Handle.Subject_code;""")
        data = {str(i+1):{'ssid':item[0],'class':item[1], 'code':item[2], 'name':item[3], 'Fname':item[4], 'Lname':item[5]} for i,item in enumerate(cur.fetchall())}
        return render(request, "admin.html", {'data':data})

    ssid = request.POST.get('ssid')
    Name = request.POST.get('Name')
    Class = request.POST.get('Class')
    Subcode = request.POST.get('Subcode')
    #Subname = request.POST.get('Subname')

    cur = connections['default'].cursor()
    cur.execute(f"INSERT INTO SUBJECT_Handle VALUES ('{ssid}', '{Class}', '{Subcode}');")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
