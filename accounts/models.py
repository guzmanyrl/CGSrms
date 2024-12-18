from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import random
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=False, null=False,unique=True)
    middle_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) 
    last_login = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    login_attempts = models.IntegerField(default=0) 
    otp_attempts = models.IntegerField(default=0)
    date_joined = models.DateTimeField(default=timezone.now)
    otp = models.CharField(max_length=6, blank=True, null=True)  # For OTP verification
    is_email_verified = models.BooleanField(default=False)
    otp_created_at = models.DateTimeField(blank=True, null=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  

    def __str__(self):
        return self.username
    
    def generate_otp(self):
        """Generate a 6-digit OTP and set its creation time."""
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()
        
    def otp_is_valid(self):
        """Check if OTP is still valid (not expired)."""
        if self.otp_created_at:
            return timezone.now() <= self.otp_created_at + timedelta(minutes=1)
        return False
    
    

    

    
    
    
