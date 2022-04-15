from django.urls import path
from . import views

urlpatterns = [
    path('', views.showMain),
    path('calendar', views.showCalendar),
    path('chart', views.showChart),
    path('media', views.showMedia),
    path('remind', views.showRemind),
]
