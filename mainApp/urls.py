from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.showMain, name='main'),
    path('calendar', views.showCalendar, name='calendar'),
    path('chart', views.showChart, name='chart'),
    path('media', views.showMedia, name='media'),
    path('remind', views.showRemind, name='remind'),
    path('diary_view/<id>/', views.showDiary_view, name='diary_view'),
    path('post', views.postDiary, name='post'),
    path('tamagotchi', views.showTamagotchi, name='tamagotchi'),
    path('share', views.showSharediary, name='share'),
    path('remove/<diary_id>', views.remove_diary, name='remove_diary'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   
