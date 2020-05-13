from django.shortcuts import render,redirect
import requests
from pprint import pprint
from .models import res, searchval, visits, Profile, bill
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User,auth
from collections import OrderedDict
from .fusioncharts import FusionCharts
import json
from django.core.mail import send_mail
from django.conf import settings
from fusionexport import ExportManager, ExportConfig
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail


# Create your views here.
def index(request):
    return render(request,"index.html")

def register(request):
    return render(request,"regform.html")

def login(request):
    if request.method == 'POST':
        uid=request.POST['uid']
        ps1=request.POST['ps']

        user=auth.authenticate(username=uid,password=ps1)
        u = user.username
        rv_li = visits.objects.filter(uid=u, checked='False')
        rs = searchval.objects.filter(uid=u).order_by('search').values_list('search', flat=True).distinct()
        if user is not None:
            auth.login(request,user)
            return render(request,'homepage.html',{'rs':rs,'rv':rv_li})
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


def rwelcome(request):
    u = request.POST.get('uid') 
    rv_li = visits.objects.filter(uid=u, checked='False')
    rs = searchval.objects.filter(uid=u).order_by('search').values_list('search', flat=True).distinct()
    return render(request,'homepage.html',{'rs':rs,'rv':rv_li})

def welcome(request):
    return render(request,'homepage.html')

def searchres(request): 
    time = datetime.now() 
    inp = 0
    if request.method == 'POST':   
        if request.POST.get('inputvalue'): 
            sval=searchval() 
            sval.uid = request.POST.get('uid') 
            sval.search= request.POST.get('inputvalue') 
            sval.time= request.POST.get(time) 
            inp = request.POST.get('inputvalue')
            sval.save() 
    res_list = res.objects.filter(cuisine__contains=inp) 
    return render(request, "searchres2.html", {'li':res_list}) 

def storevisits(request): 
    inp = 0
    if request.method == 'POST':   
        if request.POST.get('uid'): 
            vis=visits() 
            vis.uid = request.POST.get('uid') 
            vis.name= request.POST.get('resname') 
            vis.link= request.POST.get('link')
            vis.price= request.POST.get('avgp')
            vis.checked= request.POST.get('visited') 
            inp = request.POST.get('link')
            vis.save() 
    return redirect(inp)

def subbill(request):
    time = datetime.now()
    idup = request.POST.get('id')
    u = request.POST.get('uid')
    if request.method == 'POST':   
        if request.POST.get('uid'): 
            ch=bill() 
            ch.uid = request.POST.get('uid') 
            ch.name= request.POST.get('resname') 
            ch.bill= request.POST.get('bill')
            ch.time= request.POST.get(time)
            ch.save()
            vis = visits.objects.get(sid=idup)
            vis.checked = 'True'
            vis.save()
    rv_li = visits.objects.filter(uid=u, checked='False')
    rs = searchval.objects.filter(uid=u).order_by('search').values_list('search', flat=True).distinct()
    return render(request,'homepage.html',{'rs':rs,'rv':rv_li})


def chart(request):

    #Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
    dataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "MY EXPENDITURE"
    chartConfig["subCaption"] = "Powered by Bon-Appetite"
    chartConfig["xAxisName"] = "DATE"
    chartConfig["yAxisName"] = "AMOUNT"
    chartConfig["theme"] = "candy"

    current_user=request.user
    datem = datetime.today().strftime("%Y-%m")
    #month=datetime.today().strftime("%b")
    dataset = bill.objects.filter(uid=current_user.username,date__contains=datem).values('bill','date')
    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    for entry in dataset:
        usero = {}
        usero["label"]=entry['date']
        usero["value"]=int(entry['bill'])
        dataSource["data"].append(usero)

    line2D = FusionCharts("line", "Hello", "600", "400", "container", "json", dataSource)


    # Instantiate the ExportConfig class and add the required configurations
    export_config = ExportConfig()

    # Provide path of the chart configuration which we have defined above.
    # You can also pass the same object as serialized JSON.
    d=[{
        "type": "line",
        "renderAt": "container",
        "width" : "600",
        "height" : "400",
        "dataFormat": "json",
        "dataSource" : dataSource
    }]
    export_config.set('chartConfig',d)
    export_config.set("outputFile", current_user.username)


    export_server_host = "127.0.0.1"
    export_server_port = 1337

    em = ExportManager(export_server_host, export_server_port)

    em.export(export_config, output_dir = "C:\\Users\\Neha\\sem5\\zom\\bonbon", unzip = True)
    bill.img="C:\\Users\\Neha\\sem5\\zom\\bonbon\\man.png"
    
    html_content = render_to_string('mail.html')
    #html_content= '<b> This is your expenditure : </b> <img src="cid:C:\\Users\\Neha\\sem5\\zom\\export.png" >'
    text_content = strip_tags(html_content)

    # create the email, and attach the HTML version as well.
    subject = 'Thank you for registering to our site'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['jeonprerana@gmail.com','nehaprabhu8888@gmail.com']
    msg = EmailMultiAlternatives(subject, text_content, email_from,recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return render(request, 'graph.html', {'output': line2D.render() })

def lunch(request):
    res_list = res.objects.filter(cate__contains='Lunch') 
    return render(request, "searchres2.html", {'li':res_list})

def breakfast(request):
    res_list = res.objects.filter(cate__contains='Breakfast') 
    return render(request, "searchres2.html", {'li':res_list})

def dinner(request):
    res_list = res.objects.filter(cate__contains='Dinner') 
    return render(request, "searchres2.html", {'li':res_list})

def nightlife(request):
    res_list = res.objects.filter(cate__contains='Alcohol') 
    return render(request, "searchres2.html", {'li':res_list})

def cafe(request):
    res_list = res.objects.filter(cate__contains='Cafe') 
    return render(request, "searchres2.html", {'li':res_list})

def sortrate(request):
    u = request.POST.get('uid') 
    res_list = res.objects.order_by('-avg_rating')
    return render(request, "searchres2.html", {'li':res_list})

def sortprice(request):
    u = request.POST.get('uid') 
    res_list = res.objects.order_by('avg_price')
    return render(request, "searchres2.html", {'li':res_list})

def logout(request):
    auth.logout(request)
    return redirect("/")

