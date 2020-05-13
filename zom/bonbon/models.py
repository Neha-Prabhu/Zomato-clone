from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class res(models.Model):
    res_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    area = models.CharField(max_length=30)
    cuisine = models.CharField(max_length=300)
    timings = models.CharField(max_length=300, null=True)
    avg_rating = models.CharField(max_length=5)
    avg_price = models.CharField(max_length=10)
    link = models.CharField(max_length=900, null=True)
    cate = models.CharField(max_length=300, null=True)

class Profile(models.Model):
    dob = models.DateField(null=True, blank=True)
    user= models.OneToOneField(User,on_delete=models.CASCADE)

class searchval(models.Model): 
    sid = models.AutoField(primary_key=True) 
    uid = models.CharField(max_length=20, null=True) 
    search = models.CharField(max_length=200, null=False) 
    time = models.DateTimeField(auto_now_add=True, null=False) 

class visits(models.Model): 
    sid = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=20, null=True) 
    name = models.CharField(max_length=100) 
    price = models.CharField(max_length=100,null=True) 
    link = models.CharField(max_length=300, null=True) 
    checked = models.CharField(max_length=5)

class bill(models.Model): 
    sid = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=20, null=True) 
    name = models.CharField(max_length=100) 
    bill = models.CharField(max_length=100,null=True) 
    img = models.ImageField(null=True,blank=True,upload_to="images/")
    date = models.CharField(max_length=20, null=False)


