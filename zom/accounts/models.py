from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    dob = models.DateField(null=True, blank=True)
    user= models.OneToOneField(User,on_delete=models.CASCADE)