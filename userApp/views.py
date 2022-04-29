from django.shortcuts import render, redirect
from userApp.forms import SignupForm, EditProfileForm
from django.contrib import auth

from .models import Users


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=username, password=raw_password)
            # auth.login(request, user)
            return redirect("user:login")
    else:
        form = SignupForm()
    return render(request, 'userApp/signup.html', {'form': form})
            

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


def edit_profile(request):
    user = request.user

    if request.method == "POST":
        form = EditProfileForm(data=request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("user:mypage")
    else:
        form = EditProfileForm(instance=user)
    
    return render(request, "userApp/edit_profile.html", {'form': form})


def edit_password(request):
    pass


def delete(request):
    username = request.user
    user = Users.objects.get(username=username)

    user.delete()
    auth.logout(request)
    return redirect("main")

    
