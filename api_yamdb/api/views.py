from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination 

from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)
from .permissions import IsAdmin, IsModerator

class GenrePagination(PageNumberPagination):
    page_size = 10  # Установите нужное количество объектов на странице

User = get_user_model()

class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin] 
    

class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsModerator | IsAuthenticatedOrReadOnly | IsAdmin]
    pagination_class = GenrePagination
    lookup_field = 'slug'

class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений (Title)."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly | IsAdmin]
    # Укажите необходимые permission_classes здесь, если нужно

class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticatedOrReadOnly | IsAdmin]
