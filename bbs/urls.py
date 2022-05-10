from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'bbs'
urlpatterns = [
    path('', views.free, name='free'),  # 전체 게시글
    path('<int:post_id>/', views.posting, name="posting"),  # 게시글
    path('new_post/<word>/', views.new_post),  # 게시글 새로 작성
    path('<int:post_id>/remove/', views.remove_post),  # 게시글 삭제

    path(
        'comment/create/<int:post_id>/', views.comment_create,
        name='comment_create'),  # 댓글 작성
    path(
        '<int:post_id>/<int:comment_id>/',
        views.comment_delete, name="comment_delete"),  # 댓글 삭제

    path('<int:uploadfile_id>/download/', views.download, name='download'),

] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
