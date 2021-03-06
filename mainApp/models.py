from django.db import models
import os
from config import settings


class Emotion(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)


class Diary(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        "userApp.Users", on_delete=models.SET("탈퇴한 사용자"))
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=400)
    public = models.IntegerField(default=True)
    date = models.DateTimeField()
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    max_emotion = models.CharField(max_length=50, null=True)
    image = models.ImageField(blank=True, upload_to='media/')

    def delete(self, *args, **kwargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(Diary, self).delete(*args, **kwargs)


class EmotionPictures(models.Model):
    id = models.AutoField(primary_key=True)
    emotion_id = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    image = models.ImageField(null=False)


class Music(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    lyrics = models.CharField(max_length=2000)
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)


class Books(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    summary = models.CharField(max_length=50)
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)


class Movies(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    actors = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    release_year = models.CharField(max_length=50)
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)


class RecommendList(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Diary, on_delete=models.CASCADE, null=True)
    rec_movie = models.ForeignKey(Movies, on_delete=models.PROTECT, null=True)
    rec_music = models.ForeignKey(Music, on_delete=models.PROTECT, null=True)
    rec_book = models.ForeignKey(Books, on_delete=models.PROTECT, null=True)


class StoreEmotions(models.Model):
    id = models.AutoField(primary_key=True),
    emotions = models.CharField(max_length=500)
