from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import DeleteCommentView, EditCommentView


urlpatterns = [
    path('', views.ShowNewsView.as_view(), name='home'),
    path('user/<str:username>', views.UserAllNewsView.as_view(), name='user-news'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),
    path('news/<int:pk>/update', views.UpdateNewsView.as_view(), name='news-update'),
    path('news/<int:pk>/delete', views.DeleteNewsView.as_view(), name='news-delete'),
    path('news/add', views.CreateNewsView.as_view(), name='news-add'),
    path('contacts', views.contacts, name='contacts'),
    path('comment/<int:pk>/edit/', EditCommentView.as_view(), name='edit-comment'),
    path('comment/<int:pk>/delete/', DeleteCommentView.as_view(), name='delete-comment'),
    path('comment/<int:pk>/like/', views.like_comment, name='like-comment'),
    path('comment/<int:pk>/reply/', views.reply_comment, name='reply-comment'),
    path('news/<int:pk>/like/', views.like_news, name='like-news'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)