from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Diary, Emotion
from userApp.models import Users
from .forms import DiaryForm
from config import settings
import os
from django.http import HttpResponse
import urllib
from django.utils import timezone
import datetime
import requests
import json
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import re
# Create your views here.

KOBERT_API_URL = 'http://3.35.8.82:5000/kobert?text='

def showMain(request):
    current_user = Users.objects.get(id=request.user.id)
    diary = Diary.objects.filter(user_id=current_user)
    context ={
        'diary' : diary,
    }
    return render(request, 'mainApp/main.html', context)


def showCalendar(request):
    current_user = Users.objects.get(id=request.user.id)
    diary = Diary.objects.filter(user_id=current_user)
    context ={
        'diary' : diary,
    }
    return render(request, 'mainApp/calendar.html', context)


def showChart(request):
    return render(request, 'mainApp/chart.html', {})


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
    diary = Diary.objects.filter(open_status=1).order_by('-date')
    context ={
        'diary' : diary,
    }
    return render(request, 'mainApp/share.html', context)

def showDiary_view(request, id):
    showdiary = Diary.objects.get(
        id=id
        )
    diaryemotion = Emotion.objects.get(pk = showdiary.emotion_id)
    bestemotion = diaryemotion.description
    keys = []
    values = []
    emotion_list = bestemotion.split(",")
    for emotion in emotion_list :
        pair = emotion.split(":")
        keys.append(pair[0])
        values.append(pair[1])
    dict_emotion = dict(zip(keys,values))
    sort_emotion = sorted(dict_emotion.items(), key=lambda x: x[1], reverse=True)
    firstemotion = sort_emotion[0][0].replace("'",'').replace("{",'').replace("}","")
    if '행복' in firstemotion:
        emot = 0
    elif '슬픔' in firstemotion:
        emot = 1
    elif '놀람' in firstemotion:
        emot = 2
    elif '공포' in firstemotion:
        emot = 3
    elif '분노' in firstemotion:
        emot = 4
    else :
        emot = 5
    context ={
        'showdiary' : showdiary,
        'firstemotion' : firstemotion,
        'emot' : emot,
        'sort_emotion' : sort_emotion
    }
    return render(request, 'mainApp/diary_view.html', context)

def remove_diary(request, diary_id):
    diary = Diary.objects.get(id=diary_id)
    diary.delete()
    return redirect('calendar')

def postDiary(request):
    if request.method == 'POST' and request.POST['title'] != '':
        image=request.FILES['image'] if request.FILES else None
        title=request.POST['title']
        content=request.POST['content']
        try:
            open_status=request.POST['open_status']
        except:
            messages.warning(request, "공개 여부를 선택해주세요")
        date=datetime.datetime.now().strftime('%Y-%m-%d')
        api_result=requests.get(KOBERT_API_URL+content).text
        emotion = Emotion.objects.create(
            description=json.loads(api_result),
        )
        # print('cur user id:', request.user.id)
        # print('emotion:', json.loads(api_result))
        current_user = Users.objects.get(id=request.user.id)
        try:
            todaydiary = Diary.objects.get(user_id=current_user, date=date)
        except ObjectDoesNotExist:
            todaydiary = 1
        if todaydiary == 1:
            new_article=Diary.objects.create(
                    user_id=current_user,
                    title=title,
                    content=content,
                    open_status=open_status,
                    date=date,
                    image=image,
                    emotion=emotion,
                )
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