from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username= None
    objects=UserManager()
    email=models.EmailField(unique=True, null=True)
    role=models.CharField(max_length=100, unique=True, null=True)
    profile=models.BooleanField(default=False)
    first_name=models.CharField(max_length=100,null=True)
    last_name=models.CharField(max_length=100,null=True)
    father_name=models.CharField(max_length=100,null=True)
    cnic=models.IntegerField(null=True, unique=True)
    address=models.TextField(null=True)
    district=models.CharField(max_length=100,null=True)
    phone_number=models.IntegerField(null=True, unique=True)
    bio=models.TextField(null=True)
    profile_image=models.ImageField(upload_to='profile_images', null=True)
    cnic_front=models.ImageField(upload_to='cnic_images', null=True)
    cnic_back=models.ImageField(upload_to='cnic_images', null=True)  
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]