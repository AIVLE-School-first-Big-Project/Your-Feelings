from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from userApp.forms import SignupForm
from .models import Users
from django.contrib import auth


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
<<<<<<< HEAD
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=raw_password)
            auth.login(request, user)
            return redirect("main")
    else:
        form = SignupForm()
    return render(request, 'userApp/signup.html', {'form': form})
=======
            if form.password1 != password2:
                context['error'] = "비밀번호가 일치하지 않습니다."
                return render(request, "userApp/signup", context)
            else:
                form.save()
                return redirect('user:login')
        else:
            form = SignupForm()
    return render(request, 'userApp/signup.html')
>>>>>>> c86bff43381af0b1475b1ed9d23ef7c1e01ad33b
            

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
                return render(request, "userApp/login.html", context)
        except Users.DoesNotExist:
            context['error'] = "존재하지 않는 아이디입니다"
            return render(request, "userApp/login.html")
        else:
            request.session['username'] = user.username
            request.session['password'] = user.password
        return redirect("main")
    else:
        return render(request, 'userApp/login.html')

def logout(request):
    auth.logout(request)
    return redirect("main")


def mypage(request):
    user = request.user
    context = {}

    context['user'] = user

    return render(request, "userApp/mypage.html", context)


def update(request):

    username = request.user
    user = Users.objects.get(username=username)



    return render(request, "userApp/update.html")


def delete(request):
    username = request.user
    user = Users.objects.get(username=username)

    user.delete()
    auth.logout(request)
    return redirect("main")

    
