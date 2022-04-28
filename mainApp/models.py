from django.db import models

# 감정
class Emotion(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)

# 사용자가 작성한 일기들
class Diary(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey("userApp.Users", on_delete=models.SET("탈퇴한 사용자"))
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=400)
    open_status = models.IntegerField(null=True,)
    date = models.DateTimeField(null=True,)
    emotion = models.ForeignKey(Emotion, null=True, on_delete=models.PROTECT)
    image = models.ImageField(blank=True, upload_to='media/')   # 사용지가 글 쓸 때 첨부하는 사진

    

# 감정별 랜덤으로 지정해주는 사진 데베
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

# 감정 기반 추천 (일기 별로 하나)
class RecommendList(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Diary, on_delete=models.CASCADE)
    rec_movie = models.ForeignKey(Movies, on_delete=models.PROTECT)
    rec_music = models.ForeignKey(Music, on_delete=models.PROTECT)
    rec_book = models.ForeignKey(Books, on_delete=models.PROTECT)


    
    