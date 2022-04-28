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
    joy = models.IntegerField()
    anger = models.IntegerField()
    anxious = models.IntegerField()
    sad = models.IntegerField()
    surprised = models.IntegerField()
    
