from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Profile
# Create your views here.

def login(request):
    if request.method == 'POST':
        uid=request.POST['uid']
        ps1=request.POST['ps']

        user=auth.authenticate(username=uid,password=ps1)

        if user is not None:
            auth.login(request,user)
            return redirect('homepage')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')


def newreg(request):

    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        uid=request.POST['uid']
        email=request.POST['email']
        ps1=request.POST['password1']
        ps2=request.POST['password2']
        dob=request.POST['dob']
        if(len(ps1)<6):
            messages.info(request,'Enter ps more than 6')
            return redirect('newregistration')
        if ps1==ps2:
            if User.objects.filter(username=uid).exists():
                messages.info(request,'Username Taken')
                return redirect('newregistration')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already existing')
                return redirect('newregistration')
            else:
                user= User.objects.create_user(username=uid,password=ps1,email=email,first_name=fname,last_name=lname)
                newprofile=Profile(dob=dob,user=user)
                user.save()
                newprofile.save()
                print('usercreated')
                return redirect('/')
        else:
            messages.info(request,'passwords don\'t match')
            return redirect('newregistration')

    else:
        return render(request,"regform.html")


def logout(request):
    auth.logout(request)
    return redirect("/")