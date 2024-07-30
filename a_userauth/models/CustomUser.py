from a_bookmarks.models import Bookmark
from a_userauth.managers import CustomUserManager
from a_work.models import Work
from api.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    ROLE_CHOICES=[
        ('Admin', 'Admin'),
        ('Writer', 'Writer')
    ]
    
    registration_number = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True, null=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    role = models.CharField(max_length=25, blank=True, choices=ROLE_CHOICES, default="Writer")
    date_joined=models.DateTimeField(default=timezone.now)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    bookmarks= models.ManyToManyField(
        Work, 
        through=Bookmark, 
        related_name='bookmarked_by'
        )

    USERNAME_FIELD = 'registration_number'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()
    
    class Meta:
        db_table = "users"
        ordering = ("-created_at",)
        
    