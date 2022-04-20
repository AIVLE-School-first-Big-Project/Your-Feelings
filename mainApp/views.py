from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Diary
from .forms import DiaryForm
from config import settings
import os
from django.http import HttpResponse
import urllib
from django.utils import timezone
import datetime
# Create your views here.


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
        if(request.FILES):
            new_article=Diary.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            open_status=request.POST['open_status'],
            date=datetime.datetime.now(),
            image=request.FILES['image']
        )
        else:
            new_article=Diary.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            open_status=request.POST['open_status'],
            date=datetime.datetime.now(),
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