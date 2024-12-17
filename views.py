from django.shortcuts import render,redirect
from.models import Enquiry,AdminLogin,tbl_session,tbl_course,Student
import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(req):
    return render(req,"index.html")

def about(req):
    return render(req,"about.html")

def contact(req):
    return render(req,"Contact.html")
def NewsEvent(req):
    return render(req,"NewsEvent.html")

def SkillDevelopment(req):
    return render(req,"SkillDevelopment.html")

def SuccessStories(req):
    return render(req,"SuccessStories.html")



def contact(req):
    if req.method=="POST":
        name=req.POST['name']
        gender=req.POST['gender']
        address=req.POST['address']
        contactno=req.POST['contactno']
        emailaddress=req.POST['emailaddress']
        enquirydate=req.POST['enquirydate']
        enquirytext=req.POST['enquirytext']
        enquirydate=datetime.datetime.today()
        enq=Enquiry(name=name,gender=gender,address=address,contactno=contactno,emailaddress=emailaddress,enquirydate=enquirydate,enquirytext=enquirytext)
        enq.save()
        msg="Your enquiry is submitted successfull"
        return render(req,'Contact.html',{'msg':msg})
    return render(req,'Contact.html')

def login(req):
    return render(req, 'login.html')

def logcode(req):
    if req.method=="POST":
        usertype=req.POST['usertype']
        userid=req.POST['userid']
        password=req.POST['password']
        if usertype=="admin":
            try:
              user=AdminLogin.objects.get(userid=userid,password=password)
              if user is not None:
                req.session['adminid']=userid
                return redirect('adminlayout')
            except ObjectDoesNotExist:
                return render(req,'login.html',{'msg':'Invalid User'})
        elif usertype=="student": 
            try:
               stu=Student.objects.get(emailaddress=userid,password=password)
               if stu is not None:
                req.session['studentid']=userid
                return redirect('studentdash')        
            except ObjectDoesNotExist:
                return render(req,'login.html',{'msg':'Invalid User'})


def adminlayout(req):
    try:
        if req.session['adminid']!=None:
            return render(req,'adminlayout.html')
    except KeyError:
        return redirect('login')


def showenq(req):
    sh=Enquiry.objects.all()
    return render(req,'showenquiry.html',{'Show':sh})





def addsession(req):
    av=tbl_session.objects.all()
    return render(req,'addsession.html',{'Show':av})




def assave(req):
    session=req.POST['session']
    created_date=timezone.now()
    ads=tbl_session(session=session,created_date=created_date)
    ads.save()
    return redirect('addsession')

def addcourse(req):
    ch=tbl_session.objects.all()
    if req.method=="POST":
        course_session=req.POST['course_session']
        course_name=req.POST['course_name']
        course_fees=req.POST['course_fees']
        created_date=timezone.now()
        cor=tbl_course(course_session=course_session,course_name=course_name,course_fees=course_fees,created_date=created_date)
        cor.save()
        return redirect('addcourse')
    return render(req,'addcourse.html',{'ch':ch})

def courseview(req):
    ch=tbl_course.objects.all()
    return render(req,'courseview.html',{'ch':ch})


def deletecourse(req,id):
    dl=tbl_course.objects.get(pk=id)
    dl.delete()
    return redirect('courseview')

def deletesession(req,id):
    dl=tbl_session.objects.get(pk=id)
    dl.delete()
    return redirect('addsession')



def editsession(req,id):
    ab=tbl_session.objects.get(pk=id)
    if req.method=="POST":
        session=req.POST['session']
        created_date=timezone.now()
        tbl_session.objects.filter(id=id).update(session=session,created_date=created_date)
        return redirect('addsession')
    return render(req,'editsession.html',{'show':ab})



def addstudent(req):
    if req.method=="POST":
        name=req.POST['name']
        emailaddress=req.POST['emailaddress']
        contactno=req.POST['contactno']
        gender=req.POST['gender']
        stu=Student(name=name,emailaddress=emailaddress,contactno=contactno,gender=gender,password="12345",fees=0)
        stu.save()
        return redirect('addstudent')
    return render(req,'addstudent.html')


def studentdash(req):
    return render(req,'studentdash.html')

def stform(req):
    try:
        if req.session['studentid']!=None:
            stuid=req.session['studentid']
            stu=Student.objects.get(emailaddress=stuid)
            ses=tbl_session.objects.all()
            course=tbl_course.objects.all()
            return render(req,'stform.html',{'stu':stu  ,'ses':ses,'course':course})
    except KeyError:
        return redirect('login')






def saveinfo(req):
    if req.method=="POST":
        name=req.POST['name']
        fname=req.POST['fname']
        mname=req.POST['mname']
        gender=req.POST['gender']
        emailaddress=req.POST['emailaddress']
        contactno=req.POST['contactno']
        dob=req.POST['dob']
        aadharno=req.POST['aadharno']
        address=req.POST['address']
        session=req.POST['session']
        course=req.POST['course']
        hs_percent=req.POST['hs_percent']
        inter_percent=req.POST['inter_percent']
        c=tbl_course.objects.get(course_name=course)
        fees=c.course_fees
        Student.objects.filter(emailaddress=emailaddress).update(name=name,fname=fname,mname=mname,gender=gender,contactno=contactno,dob=dob,aadharno=aadharno,address=address,session=session,course=course,hs_percent=hs_percent,inter_percent=inter_percent,fees=fees)
    return redirect('stform')








def uploaddoc(req):
    if req.method=="POST":
        stuid=req.session['studentid']
        stu=Student.objects.get(emailaddress=stuid)
        pic=req.FILES['pic']
        aadharpic=req.FILES['aadharpic']
        hs_marksheet=req.FILES['hs_marksheet']
        inter_marksheet=req.FILES['inter_marksheet']
        sign=req.FILES['sign']
        fs=FileSystemStorage()
        picfile=fs.save(pic.name,pic)
        aadharfile=fs.save(aadharpic.name,aadharpic)
        hsfile=fs.save(hs_marksheet.name,hs_marksheet)
        interfile=fs.save(inter_marksheet.name,inter_marksheet)
        signfile=fs.save(sign.name,sign)
        stu.pic=picfile
        stu.aadharpic=aadharfile
        stu.hs_marksheet=hsfile
        stu.inter_marksheet=interfile
        stu.sign=signfile
        stu.application_status="C"
        stu.save()
        return redirect ('studentdash')
    




    








def orgination(req):
    return render(req,"orgination.html")

def whybtp(req):
    return render(req,"whybtp.html")

def location(req):
    return render(req,"location.html")

def certification(req):
    return render(req,"certification.html")

def coll(req):
    return render(req,"coll.html")

def network(req):
    return render(req,"network.html")

def outreach(req):
    return render(req,"outreach.html")

def ceo(req):
    return render(req,"ceo.html")

def dsm(req):
    return render(req,"dsm.html")

def science(req):
    return render(req,"science.html")


def adminis(req):
    return render(req,'adminis.html')

def tsup(req):
    return render(req,'tsup.html')

def  service(req):
    return render(req,'service.html')

def  conhall(req):
    return render(req,'conhall.html')

def  labs(req):
    return render(req,'labs.html')

def  tender(req):
    return render(req,'tender.html')

def policy(req):
    return render(req,'policy.html')

def  companies(req):
    return render(req,'companies.html')
def education(req):
    return render(req,'education.html')
def bhim(req):
    return render(req,'bhim.html')
def upskill(req):
    return render(req,'upskill.html')

def vtraning(req):
    return render(req,'vtraning.html')


def verifydoc(req):
    students=Student.objects.filter(application_status="C")
    return render(req,'verifydoc.html' , {'students':students})