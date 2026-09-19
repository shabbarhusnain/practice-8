from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.
class Education(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='education',null=True)
    Institute=models.CharField(max_length=200, null =True)
    education_type=models.CharField(max_length=50, null=True,blank=True)
    degree_name=models.CharField(max_length=100, null=True, blank=True)
    total_marks=models.FloatField(null=True, blank= True)
    obtain_marks=models.FloatField(null=True, blank=True)
    percentage=models.FloatField(null=True, blank=True)
class Category(models.Model):
    category=models.CharField(max_length=100,null=True)
    def __str__(self)->str:
        return self.category
    class Meta:
        ordering=['category']
class EducatedProfile(models.Model):
    about=models.TextField(null=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='educated_user',null=True,blank=True)
    education=models.ManyToManyField(Education, related_name='provider_education', blank=True)
    skills=models.TextField(null=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='educated_category',null=True)
    experience=models.FloatField(default=0.0)
    github=models.URLField(null=True)
    linkdin=models.URLField(null=True)
    other=models.URLField(null=True)
    def __str__(self) -> str:
        return self.user.first_name and self.user.last_name
class UneducatedProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='uneducated_user',null=True,blank=True)    
    skills=models.TextField(null=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='uneducated_category',null=True)
    experience=models.FloatField(default=0.0)
    description=models.TextField(null=True)
    def __str__(self) -> str:
        return self.user.first_name and self.user.last_name
    