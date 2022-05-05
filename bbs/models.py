from django.db import models

# Create your models here.
class Post(models.Model):
    postname = models.CharField(max_length=50)
    contents = models.TextField()
    views = models.IntegerField(default='0')
    code_edit = models.TextField(blank=True)
    writer =  models.CharField(max_length=150, blank=True)
    
    def __str__(self):
        return self.postname
    def summary(self):
        return self.contents[:80]

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    def __str__(self):
        return self.post

class UploadFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='%Y/%m/%d')
    def __str__(self):
        return self.post