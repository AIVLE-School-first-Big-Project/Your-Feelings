from .forms import UploadFileForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from config import settings
import os
from .models import UploadFile
from django.http import HttpResponse
import urllib
from django.utils import timezone
from .models import Comment
from .forms import CommentForm
from .models import Post


def free(request):
    postlist = Post.objects.order_by('-id')
    page = request.GET.get('page', '1')
    # 한 페이지에 출력할 갯수
    paginator = Paginator(postlist, 9)
    page_obj = paginator.get_page(page)

    return render(request, 'bbs/free.html', {'postlist': page_obj})


def posting(request, post_id):
    post = Post.objects.get(id=post_id)
    post.views += 1
    post.save()
    context = {
        'post': post
    }
    return render(request, 'bbs/posting.html', context)


def new_post(request, word):
    if request.method == 'POST' and request.POST['postname'] != '':
        new_article = Post.objects.create(
            postname=request.POST['postname'],
            contents=request.POST['contents'],
            code_edit=request.POST.get('code_edit', ''),
            writer=word
        )
        new_article.save()
        if(request.FILES):
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                uploadFile = form.save(commit=False)
                uploadFile.post = new_article
                uploadFile.save()
                return redirect('/free/')
        return redirect('/free/')
    elif request.method == 'POST' and request.POST['postname'] == '':
        context = {'written': request.POST['contents']}
        return render(request, 'bbs/new_post.html', context)
    else:
        form = UploadFileForm()
    return render(request, 'bbs/new_post.html')


def download(request, uploadfile_id):
    uploadFile = UploadFile.objects.get(id=uploadfile_id)
    if request.method == "GET":
        filepath = str(
            settings.BASE_DIR) + ('/media/%s' % uploadFile.file.name)
        filename = urllib.parse.quote(
            os.path.basename(filepath).encode('utf-8'))
        print(filename)
        with open(filepath, 'rb') as f:
            response = HttpResponse(f, content_type='application/octet-stream')
            response[
                'Content-Disposition'
                ] = 'attachment; filename*=UTF-8\'\'%s' % filename
            # response['Content-Disposition'] = 'attachment; filename=test.jpg'
            return response


def remove_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('/free/')
    return render(request, 'bbs/remove_post.html', {'Post': post})


def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.create_date = timezone.now()
            comment.post = post
            comment.save()
            return redirect('bbs:posting', post_id=post.id)
    else:
        form = CommentForm()
    context = {'post': post, 'form': form}
    return render(request, 'bbs/posting.html', context)


def comment_delete(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "GET":
        comment.delete()
        return redirect('bbs:posting', post_id=post.id)
    context = {'post': post, 'form': Comment.objects.all()}
    return render(request, 'bbs/posting.html', context)
