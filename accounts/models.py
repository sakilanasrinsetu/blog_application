# from rest_framework import viewsets
from django.db.models import JSONField

# from softdelete.models import SoftDeleteModel
from django.contrib.auth.base_user import BaseUserManager
from blog_application.settings import TIME_ZONE
from django.db import models
from django.contrib.auth.models import AbstractUser, User, UserManager
import uuid
from django.utils import timezone
from random import randint
from django.utils.timezone import timedelta

# Create your models here.


class UserAccount(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    full_name = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(max_length=35, unique=True)
    is_employee = models.BooleanField(default=False) # Is Staff or Not
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    objects = UserManager()