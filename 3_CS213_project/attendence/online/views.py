from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import Fac_Courses , Stud_Course ,Attendence
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import time
import csv
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "online/login_view.html" ,{"message":None})
    group1 = Group.objects.get(name='Faculty')
    group2 = Group.objects.get(name="Student")
    if group1 in request.user.groups.all():
        context = {
            "user": request.user,
            "courses": Fac_Courses.objects.filter(f_name=request.user.first_name , l_name=request.user.last_name)
        }
        return render(request , "online/faculty.html" , context)
    elif group2 in request.user.groups.all():
        stu = Stud_Course.objects.filter(rollno=request.user.username)
        empty = False
        if not stu:
            empty = True
        context = {
            "user": request.user,
            "courses": stu,
            "empty": empty
        }
        return render(request , "online/student.html" , context)
    else:
        return render(request, "online/login_view.html" ,{"message":None})

def login_view(request):
    username = request.POST.get("username",False)
    password = request.POST.get("password",False)
    user = authenticate(request , username=username , password=password)
    if user is not None:
        login(request , user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "online/login_view.html" , {"message" : "Invalid Credentials."})

@login_required
def course_detail(request,course_id):
    c = Fac_Courses.objects.get(pk=course_id)
    stu = Stud_Course.objects.filter(course=c.course_code)
    context = {
        "user" : request.user,
        "students"  : stu,
        "course_id" : course_id
    }
    return render(request , "online/course_detail.html", context)

@login_required
def register(request):
    return render(request , "online/register.html")

@login_required
def register_course(request):
    code = request.POST.get("code", False)
    name = request.POST.get("name", False)
    department = request.POST.get("department",False)
    sem = request.POST.get("sem",False)
    if Fac_Courses.objects.filter(course_code=code).exists():
        context={
        "message":"Course is already registered",
        "info"   : Fac_Courses.objects.filter(course_code=code),
        "code"   : code
        }
        return render(request , "online/register.html" ,context)
    temp = Fac_Courses(f_name=request.user.first_name,l_name=request.user.last_name,course_code=code,course_name=name,department=department,semester=sem)
    temp.save()
    context = {
        "message":"Course Registered Successfully",
        "courses": Fac_Courses.objects.filter(f_name=request.user.first_name , l_name=request.user.last_name)
    }
    return render(request, "online/faculty.html", context)

@login_required
def join_course(request,code):
    x = Fac_Courses.objects.filter(course_code=code)[0]
    if Fac_Courses.objects.filter(f_name=request.user.first_name,l_name=request.user.last_name,course_code=x.course_code).exists():
        context={
                "courses": Fac_Courses.objects.filter(f_name=request.user.first_name , l_name=request.user.last_name),
                "message2":"You are already Register in the Course "
            }
        return render(request,"online/faculty.html",context)
    temp = Fac_Courses(f_name=request.user.first_name,l_name=request.user.last_name,course_code=x.course_code,course_name=x.course_name,department=x.department,semester=x.semester)
    temp.save()
    context={
        "courses": Fac_Courses.objects.filter(f_name=request.user.first_name , l_name=request.user.last_name),
        "message":"Joined Course Successfully"
    }
    return render(request, "online/faculty.html", context)

@login_required
def enroll(request):
    course = Fac_Courses.objects.all()
    for i in course:
        for j in course:
            if i.course_code==j.course_code and i!=j:
                course = Fac_Courses.objects.exclude(f_name=j.f_name,l_name=j.l_name)
    sem = request.user.groups.filter(name__contains="Sem")
    l=[]
    for g in sem:
        l.append(g.name)
    s=l[0][-1]
    dep = request.user.groups.filter(name__contains="D-")[0].name[2:]
    course = course.filter(department__contains=dep,semester=s)
    stu = Stud_Course.objects.filter(rollno=request.user.username)
    for s in stu:
        course = course.exclude(course_code=s.course)
    empty = False
    if not course:
        empty = True
    context = {
        "course" : course,
        "empty" : empty
    }
    return render(request, "online/enroll.html", context)

@login_required
def find(request):
    dep = request.POST.get("department",False)
    sem = request.POST.get("sem",False)
    course = Fac_Courses.objects.all()
    for i in course:
        for j in course:
            if i.course_code==j.course_code and i!=j:
                course = Fac_Courses.objects.exclude(f_name=j.f_name,l_name=j.l_name)
    list = course.filter(department=dep,semester=sem)
    context = {
        "message"  : True,
        "list" : list
    }
    return render(request, "online/enroll.html", context)

@login_required
def enroll_course(request):
    course = Fac_Courses.objects.all()
    for i in course:
        for j in course:
            if i.course_code==j.course_code and i!=j:
                course = Fac_Courses.objects.exclude(f_name=j.f_name,l_name=j.l_name)
    all = Stud_Course.objects.filter(rollno=request.user.username)
    for i in course:
        if request.POST.get(i.course_code,False)=="Truee" :
            if Stud_Course.objects.filter(rollno=request.user.username,course=i.course_code).exists():
                context = {
                        "courses" : Stud_Course.objects.filter(rollno=request.user.username),
                        "m2" : "Course is already enrolled"
                }
                return render(request,"online/student.html",context)
            else:
                temp = Stud_Course(rollno=request.user.username,course=i.course_code)
                temp.save()
    context = {
        "courses" : Stud_Course.objects.filter(rollno=request.user.username),
        "m" : "Course enrolled Successfully"
    }
    return render(request,"online/student.html",context)

@login_required
def mark_attendence(request , course_idd):
    now = datetime.now()
    c = Fac_Courses.objects.get(pk=course_idd)
    stu = Stud_Course.objects.filter(course=c.course_code)
    one_hour_ago = now - timedelta(hours=1)
    chec = Attendence.objects.filter(course_code=c.course_code)
    check = chec.filter(t__range=(one_hour_ago,now))
    if check:
        diff = (now - check[0].t).total_seconds() / 60
        v = int(60-diff)
        context = {
                "user" : request.user,
                "students"  : stu,
                "course_id" : course_idd,
                "err" : "Next Attendence is only allowed after ",
                "diff": v
            }
        return render(request,"online/course_detail.html",context)
    for s in stu:
        name = s.rollno
        p = request.POST.get(name,False)
        temp = Attendence(rollno=s.rollno, course_code=c.course_code, present= p,t=datetime.now())
        temp.save()
    context = {
        "user" : request.user,
        "students"  : stu,
        "course_id" : course_idd,
        "message" : "Today's Attendence is Successfully saved."
    }
    return render(request,"online/course_detail.html" , context)

@login_required
def view_attendence(request,code):
    listi = Attendence.objects.filter(rollno=request.user.username,course_code=code)
    f = request.POST.get("from", False)
    t = request.POST.get("to", False)
    p=0
    n=0
    for i in listi:
        if i.present=="Present":
            p=p+1
        n=n+1
    if n != 0:
        percentage = (p/n)*100
        new_percentage = "{:.2f}".format(percentage)
    else:
        stu = Stud_Course.objects.filter(rollno=request.user.username)
        empty = False
        if not stu:
            empty = True
        context = {
                "user": request.user,
                "courses": stu,
                "empty": empty,
                "error": "No Attendence is Recorded for this Course!"
            }
        return render(request , "online/student.html" , context)
    if f and t:
        listi = listi.filter(date__range=[f,t])
        error = False
        if not listi:
            error="No Attendence is recorded during this period"
        context={
                "list" : listi ,
                "percent"   : new_percentage,
                "c" : code,
                "message": True,
                "error":error
        }
        return render(request,"online/view_attendence.html",context)
    context={
        "percent"   : new_percentage,
        "c" : code,
        "message": False,
    }
    return render(request ,"online/view_attendence.html" ,context)

@login_required
def view_fac(request,course_id):
    f = request.POST.get("from",False)
    t = request.POST.get("to",False)
    c = Fac_Courses.objects.get(pk=course_id)
    att = Attendence.objects.filter(course_code=c.course_code)
    if f and t:
        a_date = att.filter(date__range=[f,t]).values('date').distinct()
        r = att.filter(date__range=[f,t]).values('rollno').distinct()
        pc=[]
        for s in r:
            temp=[]
            print(s)
            listi = Attendence.objects.filter(rollno=s["rollno"], course_code=c.course_code)
            p=0
            n=0
            for i in listi:
                if i.present=="Present":
                    p=p+1
                n=n+1
            if n==0:
                temp.append("N/A")
                temp.append(s.rollno)
            else:
                percentage = (p/n)*100
                new_percentage = "{:.2f}".format(percentage)
                temp.append(new_percentage)
                temp.append(s["rollno"])
            pc.append(temp)
        context={
            "roll" : att.filter(date__range=[f,t]).values('rollno').distinct(),
            "a_date" : a_date,
            "all" : att.filter(date__range=[f,t]),
            "pc" : pc
        }
        return render(request,"online/view_fac.html",context)
    else:
        stu = Stud_Course.objects.filter(course=c.course_code)
        context = {
            "user" : request.user,
            "students"  : stu,
            "course_id" : course_id,
            "m":"Enter both From and To Dates"
        }
        return render(request,"online/course_detail.html",context)

@login_required
def stats(request):
    return render(request,"admin/stats.html")

@login_required
def find_stat_code(request):
    f = request.POST.get("from",False)
    t = request.POST.get("to",False)
    c = request.POST.get("course", False)
    att = Attendence.objects.filter(course_code=c)
    if f and t:
        a_date = att.filter(date__range=[f,t]).values('date').distinct()
        r = att.filter(date__range=[f,t]).values('rollno').distinct()
        pc=[]
        for s in r:
            temp=[]
            listi = Attendence.objects.filter(rollno=s["rollno"], course_code=c)
            p=0
            n=0
            for i in listi:
                if i.present=="Present":
                    p=p+1
                n=n+1
            if n==0:
                temp.append("N/A")
                temp.append(s.rollno)
            else:
                percentage = (p/n)*100
                new_percentage = "{:.2f}".format(percentage)
                temp.append(new_percentage)
                temp.append(s["rollno"])
            pc.append(temp)
        context={
            "roll" : att.filter(date__range=[f,t]).values('rollno').distinct(),
            "a_date" : a_date,
            "all" : att.filter(date__range=[f,t]),
            "pc" : pc,
            "c":c
            }
        return render(request, "admin/find_stat_code.html",context)
    elif not f or not t:
        context={
            "m":"Enter both From and To Dates"
        }
        return render(request, "admin/stats.html",context)
    else:
        return render(request, "admin/stats.html",context)

@login_required
def defaulter(request,code):
    att = Attendence.objects.filter(course_code=code)
    r = att.values('rollno').distinct()
    pc=[]
    for s in r:
        temp=[]
        listi = Attendence.objects.filter(rollno=s["rollno"], course_code=code)
        p=0
        n=0
        for i in listi:
            if i.present=="Present":
                p=p+1
            n=n+1
        if n==0:
            temp.append("N/A")
            temp.append(s.rollno)
        else:
            percentage = (p/n)*100
            new_percentage = "{:.2f}".format(percentage)
            temp.append(new_percentage)
            temp.append(s["rollno"])
        pc.append(temp)
    o=0
    dpc=[]
    for x in pc:
        if float(x[0]) <= 80.00:
            dpc.append(x)
        o = o+1
    context={
        "list": dpc,
        "code": code
    }
    return render(request, "admin/defaulter.html", context)

@login_required
def find_stat_roll(request):
    rollno = request.POST.get("rollno", False)
    code = request.POST.get("code", False)
    f = request.POST.get("from",False)
    t = request.POST.get("to",False)
    listi = Attendence.objects.filter(rollno=rollno, course_code=code)
    p=0
    n=0
    for i in listi:
        if i.present=="Present":
            p=p+1
        n=n+1
    if n!=0:
        percentage = (p/n)*100
        new_percentage = "{:.2f}".format(percentage)
    else:
        context={
            "error":"No Atttendence is Recorded"
        }
        return render(request,"admin/stats.html",context)
    if f and t:
        listi = listi.filter(date__range=[f,t])
        error = False
        if not listi:
            error="No Attendence is recorded during this period"
        low = False
        if float(new_percentage) <= 80:
            low = "Attendence is below or equal to 80% "
        context={
                "list" : listi ,
                "percent"   : new_percentage,
                "error2":error,
                "r" : rollno,
                "low" : low
        }
        return render(request, "admin/find_stat_roll.html", context)
    context={
        "error2" : "Enter Both From and To"
    }
    return render(request, "admin/stats.html", context)

def logout_view(request):
    logout(request)
    return render(request , "online/login_view.html", {"message" : "Logged out!"})
