from django.shortcuts import render, redirect
from userApp.forms import SignupForm, EditProfileForm
from django.contrib import auth

from .models import Users, UserEmotions


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            auth.authenticate(username=username, password=raw_password)
            # auth.login(request, user)

            UserEmotions.objects.create(
                user=Users.objects.get(username=username)
            )

            return redirect("user:login")
    else:
        form = SignupForm()
    return render(request, 'userApp/signup.html', {'form': form})


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
