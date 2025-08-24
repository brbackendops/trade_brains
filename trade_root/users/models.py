from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager , PermissionsMixin
from datetime import datetime



# Create your models here.

class CustomUserManager(BaseUserManager):
    
    
    """
        custom manager (func's) for our custom User model
    
    """
    
    def create_user(self,email,password,first_name,last_name,**other_fields):
        
        if not email:
            raise ValueError("Email is a required field")
        
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name,last_name=last_name,**other_fields)
        
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,first_name,last_name,**other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff',True)
        
        return self.create_user(email=email,password=password,first_name=first_name,last_name=last_name,**other_fields)
        


class User(AbstractBaseUser,PermissionsMixin):
    """
        extending inbuild user model class with abstract user
        changing username field (form) -> email field
        adding required fields: first_name , last_name
        
    """
    first_name = models.CharField(max_length=255,blank=False,null=False)
    last_name = models.CharField(max_length=255,blank=False,null=False) 
    
    email = models.EmailField("email",unique=True)
    designation = models.CharField(max_length=255,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name"]
        
        
    def save(self,*args,**kwargs):
        if self.password and not self.password.startswith(('pbkdf2_', 'bcrypt', 'argon2')):
            self.password = make_password(self.password)
        
        super().save(*args,**kwargs)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name
