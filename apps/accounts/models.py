from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.accounts.managers import CustomUserManager
class User(AbstractUser):
    objects=CustomUserManager()
    username=None
    email=models.EmailField(max_length=200,unique=True)
    USERNAME_FIELD='email'
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS=[]
    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    education=models.CharField(max_length=200,blank=True)
    college=models.CharField(max_length=200,blank=True)
    graduation_year=models.PositiveIntegerField(null=True,blank=True)
    github_url=models.URLField(blank=True)
    linkedin_url=models.URLField(blank=True)
    target_role=models.CharField(max_length=100,blank=True)
    experience_level=models.CharField(max_length=100,blank=True)
    bio=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.email
    
