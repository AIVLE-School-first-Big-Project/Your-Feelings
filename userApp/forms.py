from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import password_validation, update_session_auth_hash
from .models import Users
from django.core.exceptions import ValidationError

class SignupForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['full_name', 'username', 'password1']

    
    # def clean_username(self):
    #     username = self.cleaned_data('username')

    #     try:
    #         Users.objects.get(username=username)
    #         raise forms.ValidationError("이미 존재하는 아이디입니다")
    #     except:
    #         pass

    # def clean_email(self):
    #     email = self.cleaned_data('email')
    #     try:
    #         Users.objects.get(email=email)
    #         raise forms.ValidationError("이미 존재하는 아이디입니다")
    #     except:
    #         pass
    
    # def clean_password(self):
    #     password1 = self.cleaned_data('password1')
    #     password2 = self.cleaned_data('password2')
        
    #     try:
    #         password_validation.validate_password(password1, self.instnace)
    #     except:
    #         raise forms.ValidationError('8자 이상의 비밀번호로 설정해주세요')
        
    #     if password1 != password2:
    #         raise forms.ValidationError('비밀번호가 일치하지 않습니다. 다시 입력해주세요')



        # 아이디 중복 확인
        
        
        # 이메일 중복 확인
       
