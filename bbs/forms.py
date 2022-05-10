from django import forms
from .models import Comment
from .models import Post
from .models import UploadFile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postname', 'contents', 'code_edit']
        labels = {
            'postname': '제목',
            'contents': '내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '답변내용',
        }


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['file']
