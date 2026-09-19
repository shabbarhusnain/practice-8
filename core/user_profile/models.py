from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.
class UserProfile(models.Model):
    user=
    name=
    father_name=
    cnic=
    address=
    district=
    phone_number=
    bio=
    profile_image=
    cnic_front=
    cnic_back=
class SeekerProfile(models.Model):
class EducatedProfile(models.Model):
class UneducatedProfile(models.Model):