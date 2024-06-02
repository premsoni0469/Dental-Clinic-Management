
from django.shortcuts import render, redirect
from home.models import UserDetail
from home.models import UserContacts
from home.models import DoctorsMessage
from home.models import DoctorDetail
from home.models import bookappointment
from home.models import appointmenthistory
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail
import random



check_login=False
check_doclogin=False
useremail=""
doctoremail=""
uotp=""
ue=""
# --------------------------------Create your views here.-------------------------------------------------------------
# ----------------------------main homepage------------------------------
def homepage(request):
    if check_login==True:
        return redirect('userhp',useremail)
    return render(request,"index.html",{'check':check_login})


# ---------------------------contact page-----------------------------------
def contactus(request):
    
   
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('useremail')
        contact = request.POST.get('usercontact')
        message = request.POST.get('usermessage')
        
        if name == "" or email == "" or contact == "" or message == "":
            messages.warning(request,"Fill all details !")
            return redirect('contact')
        user_contact = UserContacts(name=name, email=email, contact=contact, message=message,date=datetime.today())
        user_contact.save()
        messages.success(request,"Message sent successfully")
        
        return redirect("contact")

    

    return render(request,"contactus.html",{'check':check_login,'uemail':useremail})


# -----------------------------------about page------------------------------------------
def about(request):
    return render(request,"aboutus.html",{'check':check_login,'uemail':useremail})


# ------------------------------------doctor page----------------------------------------
def fordoctor(request):
    if check_login==True:
        return redirect('userhp',useremail)
   
    if request.method == 'POST':
        if request.POST.get("form_type") == "contactOne":
            name = request.POST.get('doctorname')
            email = request.POST.get('doctoremail')
            contact = request.POST.get('doctorcontact')
            message = request.POST.get('doctormessage')
            
            if name == "" or email == "" or contact == "" or message == "":
                messages.warning(request,"Fill all details !")
                return redirect('fordoctor')
            user_contact = DoctorsMessage(name=name, email=email, contact=contact, message=message,date=datetime.today())
            user_contact.save()
            messages.success(request,"Message sent successfully")
            
            return redirect("fordoctor")
        elif request.POST.get("form_type") == "loginOne":
            demail=request.POST.get('docemail')
            dpassword=request.POST.get('docpassword')
            if demail == "" or dpassword == "":
                messages.warning(request,"Fill all details !")
                return redirect('fordoctor')
            if DoctorDetail.objects.filter(email=demail).exists():
                docotor=DoctorDetail.objects.get(email=demail)
                dp=docotor.password

                if dp==dpassword:
                    global check_doclogin
                    check_doclogin=True

                    global doctoremail
                    doctoremail=demail
                    messages.success(request,"Login successfully")
                    return redirect("doctors",demail)
                else:
                    messages.warning(request,"Password is incorrect !")
                    return redirect("fordoctor")
            else:
                messages.warning(request,"Email is not exist!")
                return redirect("fordoctor")

    return render(request,"doctorpage.html",{'check':check_login})



# -----------------------------------login-------------------------------------------
def login(request):
    global check_login
    global useremail
                    
    if check_login==True:
        return redirect('userhp',useremail)
    
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        cyah=request.POST.get('cyah')
        if email == "" or password == "":
                messages.warning(request,"Fill all details !")
                return redirect('login')
        if UserDetail.objects.filter(email=email).exists():
            user=UserDetail.objects.get(email=email)
            up=user.password

            if up==password:
                
                check_login=True
                
                useremail=email
                messages.success(request,"Login successfully")
                return redirect("userhp",email)
            else:
                messages.warning(request,"Password incorrect !")
                return redirect("login")
        else:
            messages.warning(request,"Email does not exist!")
            return redirect("login")


    return render(request,"login.html")



# ----------------------------------------------Registration---------------------------------------
def register(request):
    global check_login
    global useremail               
    if check_login==True:
        return redirect('userhp',useremail)
    
    if request.method == 'POST':
        name = request.POST.get('uname')
        email = request.POST.get('uemail')
        contact = request.POST.get('ucontact')
        dateofbirth = request.POST.get('udob')
        gender = request.POST.get('ugender')
        address = request.POST.get('uaddress')
        pincode = request.POST.get('upincode')
        password = request.POST.get('newpassword')
        cpassword =request.POST.get('confirmpassword')
        if name == "" or email == "" or contact == "" or dateofbirth == None or gender == None or address == "" or pincode == "" or password == ""or cpassword == "":
                messages.warning(request,"Fill all details !")
                return redirect('register')
        
        if password==cpassword:
            if UserDetail.objects.filter(email=email).exists():
                messages.warning(request,"Email already exist!")
                return redirect("register")
            elif UserDetail.objects.filter(contact=contact).exists():
                messages.warning(request,"Phone number already exist!")
                return redirect("register")
            else:
                user_detail = UserDetail(name=name, email=email, contact=contact, dateofbirth=dateofbirth, gender=gender, address=address, pincode=pincode, password=password)
                user_detail.save()
                
                check_login=True
                
                useremail=email
                
                send_mail(
                "Welcome to DENTIST World",
                f"Hi {name}, thank you for registering in DENTIST. We hope we can give you a beautiful smile. Thank you",
                "dentist.2407best@gmail.com",
                [email],
                fail_silently=False,
                )
                
                messages.success(request,"Registered successfully")
                return redirect("userhp",email)
        else:
            messages.warning(request,"Password does not match")
            return redirect("register")
   
    return render(request,"registrationpage.html")


    
    
# -------------------------------------------changepassword----------------------------------------------
def otp(request):
    if check_login==True:
        return redirect('userhp',useremail)
    global uotp
    global ue
    if request.method == 'POST':
       
        if request.POST.get("form_type") == "useremail":
            uemail=request.POST.get('emailid')
            if UserDetail.objects.filter(email=uemail).exists():
                udetail=UserDetail.objects.get(email=uemail)
                name=udetail.name
                otp=random.randint(10000,99999)
                
                uotp=str(otp)
                
                ue=uemail
                send_mail(
                "Verification for Changing Password",
                f"Hi {name}, your OTP(One Time Password) for changing password is {uotp} . Thank you",
                "dentist.2407best@gmail.com",
                [uemail],
                fail_silently=False,
                )

                messages.warning(request,"OTP sent to registered email ID successfully")
            else:
                messages.warning(request,"Email does not exist!")
                return redirect("otp")
        elif request.POST.get("form_type") == "changepassword":
            eotp=request.POST.get('enterotp')
            password = request.POST.get('newpassword')
            cpassword =request.POST.get('cnewpassword')
            if eotp == "" or password == "" or cpassword == "":
                    messages.warning(request,"Fill all details !")
                    return redirect('otp')
            
            if eotp == uotp:
                if password==cpassword:
                    udetail=UserDetail.objects.get(email=ue)
                    udetail.password=password
                    udetail.save()
                    
                    uotp=""
                    messages.success(request,"Password changed successfully")
                    return redirect("login")
                else:
                    messages.warning(request,"Password does not match")
                    return redirect("otp")
            else:
                messages.warning(request,"Enter correct OTP")
                return redirect("otp")


    
    return render(request,"otp.html")



#-------------------------------------------userhp-------------------------------------------
def userhomepage(request,uemailid):
    
    if check_login==False:
        return redirect('home')
    
    return render(request,"userhomepage.html",{'email':uemailid})



# ----------------------------------------appointment page------------------------------------
def appointment(request,uemailid):
    
    if check_login==False:
        return redirect('home')
    doctordetail=DoctorDetail.objects.all().order_by('name')
    

    paginator=Paginator(doctordetail, 5)
    pagenumber=request.GET.get('page')
    doctordetailfinal=paginator.get_page(pagenumber)  
    totalpage=doctordetailfinal.paginator.num_pages
    

    if request.method == 'POST':
        
        
        if request.POST.get("form_type") == "search_location":
            dlocation=request.POST.get('dlocation')
            if dlocation!=None :
                doctordetailfinal=DoctorDetail.objects.filter(city__icontains=dlocation)

        elif request.POST.get("form_type") == "search_doctor":
            dname=request.POST.get('dname')
            if dname!=None :
                doctordetailfinal=DoctorDetail.objects.filter(name__icontains=dname)
                
        elif request.POST.get("form_type") == "email_doctor":
            demail=request.POST.get('doctoremail')
            return redirect('bookappointment',demail)
       

        
    doctorinfo={
        
        'email':uemailid,
        # 'doctordetail':doctordetail,
        'lastpage':totalpage,
        
        'doctordetailfinal':doctordetailfinal,
        'totalpagelist':[n+1 for n in range(totalpage)]
        
        
    }
    return render(request,"appointmentpage.html",doctorinfo)

# ---------------------------------------book appointment----------------------------------------------
def bookuserappointment(request,demailid):
    if check_login==False:
        return redirect('home')
    
    if request.method == 'POST':
        
        
        doctordetail=DoctorDetail.objects.get(email=demailid)
        userdetail=UserDetail.objects.get(email=useremail)
        
        user_name=userdetail.name
        user_email=userdetail.email
        doctorname=doctordetail.name
        doctoremail=doctordetail.email
        clinicname=doctordetail.clinicname
        city=doctordetail.city
        consultationfee=doctordetail.consultationfee
        apdate = request.POST.get('ad')
        aptime = request.POST.get('select_time')
        payment = request.POST.get('select_payment')
        
        date=str(datetime.today())
        
        
        if apdate!=None and aptime!=None and payment!=None:
            if apdate > date or apdate == date:
                if bookappointment.objects.filter(doctoremail=demailid,appdate=apdate,apptime=aptime).exists():
                    messages.warning(request,"Please change appointment date or time. Doctor is not available")
                    return redirect('bookappointment',doctoremail)
                
                if bookappointment.objects.filter(appdate=apdate,useremail=user_email).exists():
                    messages.warning(request,"Please change date. You have already booked an appointment on selected date.")
                    return redirect('bookappointment',doctoremail)
                 
                user_appoint = bookappointment(username=user_name, useremail=user_email, doctorname=doctorname, doctoremail=doctoremail,clinicname=clinicname,city=city, appdate=apdate, apptime=aptime, consultationfee=consultationfee, payment=payment)
                user_appoint.save()
                send_mail(
                "Appointment Confirmation",
                f"Hi {user_name}, Your appointment is confirmed with Dentist {doctorname} on {apdate} at {aptime}. Address of dentist is {clinicname}, {city} and dentist consultation fee is {consultationfee}. Be on time please. Thank you",
                "dentist.2407best@gmail.com",
                [user_email],
                fail_silently=False,
                )
                messages.success(request,"Appointment booked successfully")
                
                return redirect('appointment',useremail)
            else:
                messages.success(request,"Select valid date!")
                
                return redirect('bookappointment',doctoremail)
        else:
            messages.success(request,"Select all the fields!")
            
            return redirect('bookappointment',doctoremail)
    return render(request,"bookappointment.html",{'demail':demailid})


# ----------------------------------emergency appointment page----------------------------------------------
def emergencyappointment(request,uemailid):
    
    if check_login==False:
        return redirect('home')
    doctordetail=DoctorDetail.objects.all().order_by('name')
    

    paginator=Paginator(doctordetail, 5)
    pagenumber=request.GET.get('page')
    doctordetailfinal=paginator.get_page(pagenumber)  
    totalpage=doctordetailfinal.paginator.num_pages
    

    if request.method == 'POST':
        
        
        if request.POST.get("form_type") == "search_location":
            dlocation=request.POST.get('dlocation')
            if dlocation!=None :
                doctordetailfinal=DoctorDetail.objects.filter(city__icontains=dlocation)

        elif request.POST.get("form_type") == "search_doctor":
            dname=request.POST.get('dname')
            if dname!=None :
                doctordetailfinal=DoctorDetail.objects.filter(name__icontains=dname)
                
        elif request.POST.get("form_type") == "email_doctor":
            demail=request.POST.get('doctoremail')
            return redirect('bookemergencyappointment',demail)
       

        
    doctorinfo={
        
        'email':uemailid,
        # 'doctordetail':doctordetail,
        'lastpage':totalpage,
        'doctordetailfinal':doctordetailfinal,
        'totalpagelist':[n+1 for n in range(totalpage)]
        
        
    }
    return render(request,"emergencyappointmentpage.html",doctorinfo)

# -------------------------------------book emergency appointment--------------------------------------------------
def bookemergencyappointment(request,demailid):
    if check_login==False:
        return redirect('home')
    
    date=str(datetime.today())
    todaysdate=date[0:10]
        
    if request.method == 'POST':
        
        
        doctordetail=DoctorDetail.objects.get(email=demailid)
        userdetail=UserDetail.objects.get(email=useremail)
        
        user_name=userdetail.name
        user_email=userdetail.email
        doctorname=doctordetail.name
        doctoremail=doctordetail.email
        clinicname=doctordetail.clinicname
        city=doctordetail.city
        consultationfee=doctordetail.consultationfee
        consultfee=consultationfee+" + 150"
        aptime = request.POST.get('select_time')
        payment = request.POST.get('select_payment')
        
        
        
        if aptime!=None and payment!=None:
            if bookappointment.objects.filter(doctoremail=demailid,appdate=todaysdate,apptime=aptime).exists():
                appdetail=bookappointment.objects.get(doctoremail=demailid,appdate=todaysdate,apptime=aptime)
                cuser_name=appdetail.username
                cuser_email=appdetail.useremail
                consultationfee=appdetail.consultationfee
                t=aptime[0:2]+":30 "+aptime[6:8]
                upayment=appdetail.payment
                user_appoint = bookappointment(username=cuser_name, useremail=cuser_email, doctorname=doctorname, doctoremail=doctoremail,clinicname=clinicname,city=city, appdate=todaysdate, apptime=t, consultationfee=consultationfee, payment=upayment)
                user_appoint.save()   
                appdetail.delete()
                send_mail(
                "Appointment Confirmation",
                f"Hi {cuser_name}, Your appointment time with Dentist {doctorname} on {todaysdate} at {aptime} is postponed due to emergency! The revised appointment time is {t}. Address of dentist is {clinicname}, {city} and dentist consultation fee is {consultationfee}. Be on time please. Sorry for the inconvenience. Thank you",
                "dentist.2407best@gmail.com",
                [cuser_email],
                fail_silently=False,
                )
                
            if bookappointment.objects.filter(appdate=todaysdate,useremail=user_email).exists():
                messages.warning(request,"You cannot take an appointment. You already booked an appointment on selected date.")
                return redirect('bookemergencyappointment',doctoremail)
                
            user_appoint = bookappointment(username=user_name, useremail=user_email, doctorname=doctorname, doctoremail=doctoremail,clinicname=clinicname,city=city, appdate=todaysdate, apptime=aptime, consultationfee=consultfee, payment=payment)
            user_appoint.save()
            send_mail(
                "Appointment Confirmation",
                f"Hi {user_name}, Your appointment is confrimed with Dentist {doctorname} on {todaysdate} at {aptime}. Address of dentist is {clinicname}, {city} and dentist consultation fee is {consultfee}. Be on time please. Thank you.",
                "dentist.2407best@gmail.com",
                [user_email],
                fail_silently=False,
                )
            messages.success(request,"Appointment booked successfully")
            
            return redirect('userhp',useremail)
            
        else:
            messages.success(request,"Select all the fields!")
            
            return redirect('bookemergencyappointment',doctoremail)
    return render(request,"bookemergencyappointment.html",{'demail':demailid,'date':todaysdate})



# -----------------------------------user current appointment list----------------------------------------------
def appointmentlist(request,uemailid):
    if check_login==False:
        return redirect('home')
    
    cdate=str(datetime.today())
    appdetail=bookappointment.objects.filter(useremail=uemailid).order_by('appdate')
    noappointment=True
    if not appdetail:
        noappointment=False
    
    info={
        'noappointment':noappointment,
        'email':uemailid,
        'appdetail':appdetail,
        'currentdate':cdate
        
    }
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        doctorname = request.POST.get('doctorname')
        appdetail= bookappointment.objects.get(useremail=uemailid,appdate=date,apptime=time,doctorname=doctorname)
        user_name=appdetail.username
        
        appdetail.delete()
        send_mail(
                "Appointment Cancelled",
                f"Hi {user_name}, Your appointment is cancelled with Dentist {doctorname} on {date} at {time} successfully. Thank you.",
                "dentist.2407best@gmail.com",
                [uemailid],
                fail_silently=False,
                )
        messages.success(request,"Appointment cancelled successfully!")
        return redirect('applist',uemailid)
    return render(request,"appointmentlist.html",info)


# ---------------------------------------------user history list------------------------------------------------------
def history(request,uemailid):
    if check_login==False:
        return redirect('home')
    userdetail=appointmenthistory.objects.filter(useremail=uemailid)
    noappointment=True
    if not userdetail:
        noappointment=False
    userinfo={
        'noappointment':noappointment,
        'email':uemailid,
        'userdetail':userdetail
    }

    return render(request,"userhistory.html",userinfo)


# -------------------------------------------user detail----------------------------------------------------------
def userdetail(request,uemailid):
    if check_login==False:
        return redirect('home')
    userdetail=UserDetail.objects.get(email=uemailid)
    userinfo={

        'email':uemailid,
        'userdetail':userdetail
    }
    
    return render(request,"userdetail.html",userinfo)


# -----------------------------------------doctor schedule page----------------------------------------------------
def doctorschedule(request,demail):
    if check_doclogin==False:
        return redirect('home')
    
    tdate=str(datetime.today())
    todaysdate=tdate[0:10]
    
    userdetail=bookappointment.objects.filter(doctoremail=demail,appdate=todaysdate).order_by('apptime')
    noappointment=True
    if not userdetail:
        noappointment=False
    userinfo={
        'noappointment':noappointment,
        'email':demail,
        'userdetail':userdetail
    }

    if request.method == 'POST':
        if request.POST.get("form_type") == "email_user":
            date = request.POST.get('date')
            time = request.POST.get('time')
            useremail = request.POST.get('useremail')
            doctorname = request.POST.get('doctorname')
            
            appdetail= bookappointment.objects.get(useremail=useremail,appdate=date,apptime=time,doctorname=doctorname)
            user_name=appdetail.username
            appdetail.delete()
            send_mail(
                "Appointment Cancelled",
                f"Hi {user_name}, Your appointment with Dentist {doctorname} on {date} at {time} is cancelled. Reason: Absent. Thank you.",
                "dentist.2407best@gmail.com",
                [useremail],
                fail_silently=False,
                )
            messages.success(request,"Appointment cancelled successfully!")
            return redirect('doctors',demail)
        
        elif request.POST.get("form_type") == "prescription":
            uemail=request.POST.get('useremail')
            
            
            return redirect('prescription',uemail)

    
    return render(request,"doctorschedule.html",userinfo)


# ---------------------------------------------------prescription---------------------------------------------------------
def prescription(request,uemail):
    if check_doclogin==False:
        return redirect('home')
    userdetail=UserDetail.objects.get(email=uemail)
    tdate=str(datetime.today())
    todate=tdate[0:4]
    
    dob=userdetail.dateofbirth
    doy=dob[0:4]
    
    age=int(todate) - int(doy)
    userinfo={
        'age':age,
        'email':uemail,
        'userdetail':userdetail
    }
    todaysdate=tdate[0:10]

    if request.method == 'POST':
        prescription=request.POST.get('pres')
        if prescription == "":
            messages.warning(request,"Please write prescription!")
            return redirect('prescription',uemail)
        doctordetail=DoctorDetail.objects.get(email=doctoremail)
        userdetail=UserDetail.objects.get(email=uemail)
        appdetail=bookappointment.objects.get(useremail=uemail,doctoremail=doctoremail,appdate=todaysdate)
        user_name=userdetail.name
        user_email=userdetail.email
        doctorname=doctordetail.name
        docemail=doctordetail.email
        
        date=appdetail.appdate
        time=appdetail.apptime
        payment=appdetail.payment
        consultationfee=doctordetail.consultationfee

        user_appoint = appointmenthistory(username=user_name, useremail=user_email, doctorname=doctorname, doctoremail=docemail,appdate=date, apptime=time, consultationfee=consultationfee, payment=payment,prescription=prescription)
        user_appoint.save()
        appdetail= bookappointment.objects.get(useremail=user_email,appdate=date,doctorname=doctorname)
        appdetail.delete()
        messages.success(request,"Appointment completed! ")
        
        return redirect('doctors',docemail)

    return render(request,"prescription.html",userinfo)

# -------------------------------------------logout---------------------------------------------------
def userlogout(request):
    global check_login
    check_login=False
    global check_doclogin
    check_doclogin=False
    messages.success(request,"Log out successfully")
    
    return redirect("home")