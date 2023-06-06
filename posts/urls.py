from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.GetAllPosts.as_view()),
    path('posts/create', views.PostCreate.as_view()),
    path('posts/<int:pk>/delete', views.PostDelete.as_view()),
    path('comment/', views.CommentCreate.as_view()),
    path('comment/<int:pk>/delete', views.CommentDelete.as_view()),
    path('post/<int:pk>/edit', views.PostEdit.as_view()),
]
