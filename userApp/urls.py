from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='userApp/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path("mypage/", views.mypage, name='mypage')
]