from math import fabs
from django.db import models
from django.contrib.auth.models import AbstractUser
from sqlalchemy import false

# Create your models here.
class Users(AbstractUser):
    full_name = models.CharField(max_length=100)
    first_name = None
    last_name = None
    email = models.EmailField(blank=False, unique=True)
    username = models.CharField(max_length=100, blank=False, unique=True)
