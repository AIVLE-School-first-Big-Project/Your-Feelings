from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Users
from django.contrib import auth


def signup(request):
    if request.method == "POST":
        pw1 = request.POST.get("password")
        pw2 = request.POST.get("password2")

        if pw1 == pw2:
            user = Users.objects.create_user(
                username = request.POST.get("username"),
                password = request.POST.get("password"),
                email = request.POST.get("email"),
                full_name = request.POST.get("full_name")
            )
            auth.login(request, user)
            return redirect("user:login")
        else:
            return render(request, "userApp/signup.html", {'error': "비밀번호가 일치하지 않습니다"})
    return render(request, "userApp/signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        context = {}

        try:
            user = Users.objects.get(username=username)
            context['username'] = username

            if password != user.password:
                context['error'] = "비밀번호가 틀렸습니다"
                return render(request, "userApp/login.html")
        except Users.DoesNotExist:
            context['error'] = "존재하지 않는 아이디입니다"
            return render(request, "userApp/login")
        else:
            request.session['username'] = user.username
            request.session['password'] = user.password
        return redirect("main")
    else:
        return render(request, 'userApp/login.html')

def logout(request):
    return render(request, 'userApp/logout.html')
