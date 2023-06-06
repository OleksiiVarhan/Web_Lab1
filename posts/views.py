from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrSuperuser, IsOwnerOrSuperuserOrPostOwner


class GetAllPosts(GenericAPIView):

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        posts = Post.objects.filter(author=user)
        posts = [post_to_json(post) for post in posts]
        return Response(posts)


class PostCreate(GenericAPIView):
    serializer_class = PostSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(post_to_json(post))
        return Response(status=400)


def post_to_json(model):
    return {'author': model.author.id, 'title': model.title, 'text': model.text,
                        'created_at': model.created_at}


def comment_to_json(model):
    return {'content': model.content,
                        'to_post': model.to_post.id}


class PostDelete(GenericAPIView):

    def delete(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        post.delete()
        return Response(status=204)


class CommentDelete(GenericAPIView):

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        comment.delete()
        return Response(status=204)


class CommentCreate(GenericAPIView):
    serializer_class = CommentSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save()
            return Response(comment_to_json(comment))
        return Response(status=400)


class PostEdit(GenericAPIView):
    serializer_class = PostSerializer

    def put(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post.text = serializer.data['text']
            post.title = serializer.data['title']
            post.save()
            return Response(post_to_json(post))
        return Response(status=400)
