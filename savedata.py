import django
import os
import pandas as pd
from tqdm import tqdm
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from mainApp.models import Music, Books, Movies, Emotion, Diary, RecommendList
from bbs.models import Post, Comment, UploadFile
from userApp.models import Users

def calculateMin(objects, emotion):
    keys = ['공포','놀람','분노','슬픔','행복']
    val = float('inf')
    target = None
    for i in tqdm(objects):
        target_emo = eval(Emotion.objects.get(id=i.emotion_id).description)
        diary_emo = emotion.description
        hap = sum((target_emo[key]-diary_emo[key])**2 for key in keys)
        if val > hap:
            val = hap
            target = i
            # print(val, i.title)
    return target
def getRecommendation(emotion):
    books = Books.objects.all()
    movies = Movies.objects.all()
    music = Music.objects.all()
    for i in [movies, music, books]:
        yield calculateMin(i, emotion)

KOBERT_URL = 'http://3.35.8.82:5000/kobert?text='
BERT_URL = 'http://3.35.8.82:5000/bert?text='
def getEmotionsFromAPI(model='kobert', text=''):
    url = KOBERT_URL if model=='kobert' else BERT_URL
    res = requests.get(url + text).text
    return json.loads(res)

def diary():
    # data = pd.read_csv('diary_data.csv')
    # for i in data.to_dict('records'):
    
    for i in Diary.objects.all():
        emotion = Emotion(description=getEmotionsFromAPI('kobert', i.content))
        emotion.save()
        new_diary = Diary(
            title=i.title, 
            content=i.content, 
            public=i.public, 
            date=i.date, 
            image=i.image, 
            emotion=emotion,
            user_id=i.user_id, 
            max_emotion=sorted(emotion.description.items(), key=lambda x:-x[1])[0][0]
            )
        new_diary.save()
        print(new_diary)
        # new_diary = Diary.objects.create(
        #     title = i['title'],
        #     content = i['content'],
        #     public = i['public'],
        #     date = i['date'],
        #     image = i['image'],
        #     emotion = emotion,
        #     user_id = Users.objects.get(username=i['user_id']),
        #     max_emotion = sorted(emotion.description.items(), key=lambda x:-x[1])[0][0]
        # )
        # # print(i.title, i.user_id, sorted(emotion.description.items(), key=lambda x:-x[1])[0][0])
        movie, music, book = getRecommendation(emotion)
        RecommendList.objects.create(
            post_id = new_diary,
            rec_movie = movie,
            rec_music = music,
            rec_book = book,
        )

diary()

def save_diary():
    all_diary = Diary.objects.all()
    data =[]
    for i in all_diary:
        tmp = {
            'title':i.title,
            'content':i.content,
            'public':i.public,
            'date':i.date,
            'image':i.image,
            'user_id':i.user_id,
            
        }
        data.append(tmp)
    
    df = pd.DataFrame(data)
    df.to_csv('diary_data.csv', index=False)

# save_diary()