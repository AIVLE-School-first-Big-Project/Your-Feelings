from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser):
    full_name = models.CharField(max_length=50)
    first_name = None
    last_name = None
