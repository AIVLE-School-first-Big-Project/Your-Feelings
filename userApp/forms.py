from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Users


class SignupForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=50, required=True, help_text="이름을 입력해주세요")
    email = forms.EmailField(
        max_length=100, required=True, help_text="유효한 이메일을 입력해주세요")

    class Meta:
        model = Users
        fields = ['full_name', 'username', 'password1', 'password2', 'email']

        labels = {
            'username': '아이디',
            'password1': '비밀번호',
            'email': '이메일',
            'full_name': '이름',
        }


class EditProfileForm(UserChangeForm):
    full_name = forms.CharField(
        max_length=50, required=True, help_text="이름을 입력해주세요")
    email = forms.EmailField()

    class Meta:
        model = Users
        fields = ['full_name', 'email']
