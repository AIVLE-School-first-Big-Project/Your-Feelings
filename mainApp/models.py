from django.db import models

# Create your models here.
class Diary(models.Model):
    user_id = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=400)
    open_status = models.IntegerField()
    date = models.DateTimeField()
    emotion = models.CharField(max_length=50)