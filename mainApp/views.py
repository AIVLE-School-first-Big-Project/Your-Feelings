from django.shortcuts import render, redirect
from .models import *
from userApp.models import UserEmotions, Users
from .forms import DiaryForm
from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta
import requests
import json
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import random
from tqdm import tqdm
# Create your views here.

KOBERT_API_URL = 'http://3.35.8.82:5000/kobert?text='



def showMain(request):
    context ={}
    try:
        current_user = Users.objects.get(id=request.user.id)
        diary = Diary.objects.filter(user_id=current_user)
        context['diary'] = diary
    except:
        pass
    return render(request, 'mainApp/main.html', context)


def showCalendar(request):
    current_user = Users.objects.get(id=request.user.id)
    diary = Diary.objects.filter(user_id=current_user)
    context ={
        'diary' : diary,
    }
    return render(request, 'mainApp/calendar.html', context)


def showChart(request):
    user_id = request.user.id
    context = {}
    
    # donut chart
    user_emotions = UserEmotions.objects.get(user_id=user_id)

    # line chart
    end_date = timezone.now() + relativedelta(days=1)
    start_date = end_date - relativedelta(months=6)

    diaries = Diary.objects.filter(
        user_id_id = user_id,
        date__range=[start_date, end_date]
    )

    monthly_happy = {}
    monthly_sad = {}
    monthly_angry = {}
    for i in range(5, -1, -1):
        m = (timezone.now() - relativedelta(months=i)).strftime("%Y/%m")
        monthly_happy[m] = 0
        monthly_sad[m] = 0
        monthly_angry[m] = 0

    
    for d in diaries:
        month = d.date.strftime("%Y/%m")
        emotion = d.max_emotion

        if emotion == "행복":
            monthly_happy[month] += 1
        elif emotion == "슬픔":
            monthly_sad[month] += 1
        elif emotion == "분노":
            monthly_angry[month] += 1

    months = []
    happy_cnt = []
    for mth, cnt in monthly_happy.items():
        months.append(mth)
        happy_cnt.append(cnt)

    sad_cnt = []
    for _, cnt in monthly_sad.items():
        sad_cnt.append(cnt)
    
    angry_cnt = []
    for _, cnt in monthly_angry.items():
        angry_cnt.append(cnt)

    # context
    context = {
        'user_emotions': user_emotions,
        'diaries': diaries,
        'months': months,
        'happy_cnt': happy_cnt,
        'sad_cnt': sad_cnt,
        'angry_cnt': angry_cnt
    }    

    return render(request, 'mainApp/chart.html', context)



def showMedia(request):
    return render(request, 'mainApp/media.html', {})


def showRemind(request):
    current_user = Users.objects.get(id=request.user.id)
    diary = Diary.objects.filter(user_id=current_user).order_by('-date')
    context ={
        'diary' : diary,
    }
    return render(request, 'mainApp/remind.html', context)


def showSharediary(request):
    current_user = Users.objects.get(id=request.user.id)
    diary = Diary.objects.filter(public=1).order_by('-date')
    context ={
        'diary' : diary,
    }
    return render(request, 'mainApp/share.html', context)


def showDiary_view(request, id):
    showdiary = Diary.objects.get(
        id=  id
        )
    diaryemotion = Emotion.objects.get(pk = showdiary.emotion_id)
    bestemotion = diaryemotion.description
    keys = []
    values = []
    emotion_list = bestemotion.split(",")
    for emotion in emotion_list :
        print(emotion)
        pair = emotion.split(":")
        keys.append(pair[0])
        values.append(pair[1])
    dict_emotion = dict(zip(keys,values))
    sort_emotion = sorted(dict_emotion.items(), key=lambda x: x[1], reverse=True)
    firstemotion = sort_emotion[0][0].replace("'",'').replace("{",'').replace("}","")

    emoticon_dict ={
        '분노': ['anger_1', 'anger_2'],
        '혐오': ['disgust_1','disgust_2','disgust_3','disgust_4'],
        '공포': ['fear_1'],
        '행복': ['joy_1', 'joy_2', 'joy_3', 'joy_4', 'joy_5'],
        '중립': ['neutral_1', 'neutral_2', 'neutral_3'],
        '슬픔': ['sadness_1', 'sadness_2', 'sadness_3'],
        '놀람': ['surprise_1']
    }
    try:
        recommended = RecommendList.objects.get(post_id=showdiary)
    except:
        recommended = None
        
    context ={
        'showdiary' : showdiary,
        'firstemotion' : firstemotion,
        'emoticon' : random.choice(emoticon_dict[firstemotion.strip()]),
        'recommended' : recommended
        # 'firstvalue' : firstvalue,
        # 'secondemotion' : secondemotion,
        # 'secondvalue' : secondvalue,
        # 'thirdemotion' : thirdemotion,
        # 'thirdvalue' : thirdvalue,
    }
    
    return render(request, 'mainApp/diary_view.html', context)


def calculateMin(objects, emotion):
    keys = ['공포','놀람','분노','슬픔','중립','행복','혐오']
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
    # book = random.choice(Books.objects.all())
    # movie = random.choice(Movies.objects.all())
    # music = random.choice(Music.objects.all())


def remove_diary(request, diary_id):
    diary = Diary.objects.get(id=diary_id)
    emotion = Emotion.objects.get(id=diary.emotion_id)
    emotion.delete()
    diary.delete()


    return redirect('calendar')


def postDiary(request):
    if request.method == 'POST' and request.POST['title'] != '':
        image=request.FILES['image'] if request.FILES else None
        title=request.POST['title']
        content=request.POST['content']
        public=request.POST['public']
        
        date=datetime.datetime.now().strftime('%Y-%m-%d')
        api_result=requests.get(KOBERT_API_URL+content).text

        description = json.loads(api_result)

        emotion = Emotion.objects.create(
            description = description,
        )

        max_emotion = max(description, key=description.get)
        current_user = Users.objects.get(id=request.user.id)

        user_emotions = UserEmotions.objects.get(user_id=request.user.id)
        if max_emotion  == '공포':
            user_emotions.terrified += 1
            user_emotions.save()
        elif max_emotion == "놀람":
            user_emotions.surprised += 1
            user_emotions.save()
        elif max_emotion == "슬픔":
            user_emotions.sad += 1
            user_emotions.save()
        elif max_emotion == "중립":
            user_emotions.neutral += 1
            user_emotions.save()
        elif max_emotion == "행복":
            user_emotions.happy += 1
            user_emotions.save()
        else:
            user_emotions.hate += 1
            user_emotions.save()


        try:
            todaydiary = Diary.objects.get(user_id=current_user, date=date)
        except ObjectDoesNotExist:
            todaydiary = 1
        if todaydiary == 1:
            new_article=Diary.objects.create(
                    user_id=current_user,
                    title=title,
                    content=content,
                    public=public,
                    date=date,
                    image=image,
                    emotion=emotion,
                    max_emotion = max_emotion
                )
            movie, music, book = getRecommendation(emotion)
            RecommendList.objects.create(
                post_id = new_article,
                rec_movie = movie,
                rec_music = music,
                rec_book = book,
                ).save()
            new_article.save()
            return redirect('calendar')
        else :
            messages.warning(request, "이미 작성한 다이어리가 있어요.")
            return redirect('calendar')                
    elif request.method == 'POST' and request.POST['title'] == '' :
        context = {'written' : request.POST['content']}
        return render(request, 'mainApp/diary_post.html', context)
    else:
        form = DiaryForm()
    return render(request, 'mainApp/diary_post.html')


def showTamagotchi(request):
    now_user = Users.objects.get(id=request.user.id)
    totaldiary = Diary.objects.filter(user_id=now_user)
    duringtime = now_user.last_login - now_user.date_joined
    totaldiarynum = len(totaldiary)
    point = duringtime.days + totaldiarynum
    daypercent = duringtime.days/365*100
    context ={
        'duringtime' : duringtime.days,
        'totaldiary' : totaldiarynum,
        'point' : point,
        'daypercent' : daypercent,
    }
    return render(request, 'mainApp/tamagotchi.html', context)