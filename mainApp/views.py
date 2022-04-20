from django.shortcuts import render

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


def showTamagotchi(request):
    return render(request, 'mainApp/tamagotchi.html', {})