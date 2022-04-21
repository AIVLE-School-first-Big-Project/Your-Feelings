from django import forms

from .models import Diary
class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'content','open_status','image']
        
        labels = {
            'title': '제목',
            'content': '내용',
            'open_status' : '공개여부',
        }