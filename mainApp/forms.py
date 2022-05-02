from django import forms

from .models import Diary
class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'content','public','image']
        
        labels = {
            'title': '제목',
            'content': '내용',
            'public' : '공개여부',
        }