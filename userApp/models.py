from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser):
    full_name = models.CharField(max_length=100)
    first_name = None
    last_name = None
    email = models.EmailField(blank=False, unique=True)
    username = models.CharField(max_length=100, blank=False, unique=True)


class UserEmotions(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    terrified = models.IntegerField(default=0)
    surprised = models.IntegerField(default=0)
    angry = models.IntegerField(default=0)
    sad = models.IntegerField(default=0)
    neutral = models.IntegerField(default=0)
    happy = models.IntegerField(default=0)
    hate = models.IntegerField(default=0)
    
