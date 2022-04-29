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
# Create your views here.

KOBERT_API_URL = 'http://3.34.5.170:5000/kobert?text='

def showMain(request):
    return render(request, 'mainApp/main.html', {})


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

def showDiary_view(request, id):
    showdiary = Diary.objects.get(
        id=id
        )
    #diaryemotion = Emotion.objects.get(pk = showdiary.emotion_id)
    context ={
        'showdiary' : showdiary,
        #'diaryemotion' : diaryemotion
    }
    return render(request, 'mainApp/diary_view.html', context)

def postDiary(request):
    if request.method == 'POST' and request.POST['title'] != '':
        image=request.FILES['image'] if request.FILES else None
        title=request.POST['title']
        content=request.POST['content']
        open_status=request.POST['open_status']
        date=datetime.datetime.now().strftime('%Y-%m-%d')
        #api_result=requests.get(KOBERT_API_URL+content).text
        #emotion = Emotion.objects.create(
        #    description=json.loads(api_result),
        #)
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
                    #emotion=emotion,
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