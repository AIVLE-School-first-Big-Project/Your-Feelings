from django.urls import path
from . import views

urlpatterns = [
    path('', views.showMain, name='main'),
    path('calendar', views.showCalendar, name='calendar'),
    path('chart', views.showChart, name='chart'),
    path('media', views.showMedia, name='media'),
    path('remind', views.showRemind, name='remind'),
    path('diary_view', views.showDiary_view, name='diary_view'),
]
