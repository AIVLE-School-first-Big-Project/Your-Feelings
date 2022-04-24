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
# Create your views here.

API_URL = 'http://3.34.5.170:5000/api?text='

def showMain(request):
    return render(request, 'mainApp/main.html', {})


def showCalendar(request):
    return render(request, 'mainApp/calendar.html', {})


def showChart(request):
    return render(request, 'mainApp/chart.html', {})


def showMedia(request):
    return render(request, 'mainApp/media.html', {})


def showRemind(request):
    return render(request, 'mainApp/remind.html', {})

def showDiary_view(request):
    return render(request, 'mainApp/diary_view.html', {})

def postDiary(request):
    if request.method == 'POST' and request.POST['title'] != '':
        image=request.FILES['image'] if request.FILES else None
        title=request.POST['title']
        content=request.POST['content']
        open_status=request.POST['open_status']
        date=datetime.datetime.now()
        api_result=requests.get(API_URL+content).text
        emotion = Emotion.objects.create(
            description=json.loads(api_result),
        )
        # print('cur user id:', request.user.id)
        # print('emotion:', json.loads(api_result))
        
        current_user = Users.objects.get(id=request.user.id)
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
        return redirect('/main/')
    elif request.method == 'POST' and request.POST['title'] == '' :
        context = {'written' : request.POST['content']}
        return render(request, 'mainApp/diary_post.html', context)
    else:
        form = DiaryForm()
    return render(request, 'mainApp/diary_post.html')


def showTamagotchi(request):
    return render(request, 'mainApp/tamagotchi.html', {})