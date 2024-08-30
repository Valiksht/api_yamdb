
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework import viewsets
from reviews.models import Category, Genre, Title, Review, Comment
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework.permissions IsAdminUser
from .serializers import ReviewSerializer, CommentSerializer, UserSerializer
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .permissions import IsAdmin


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class UserViewSet(viewsets.ModelViewSet):
    """Вункция работающая с моделью пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin | IsAuthenticatedOrReadOnly]
