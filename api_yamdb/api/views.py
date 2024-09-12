from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, DestroyModelMixin
)

from api_yamdb.constants import MEUSERNAME
from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (
    ReviewSerializer, CommentSerializer, UserSerializer,
    CategorySerializer, GenreSerializer, TitleSerializer,
    ReadTitleSerializer
)
from .permissions import AdminOnly, AdminOrReadOnly, AdminModeratorOrReadOnly
from .filters import TitleFilter


User = get_user_model()


class CategoryViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)


class GenreViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений (Title)."""

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    filter_backends = (DjangoFilterBackend,)
    permission_classes = [AdminOrReadOnly]
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ReadTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AdminModeratorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(
            author=self.request.user, title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AdminModeratorOrReadOnly]

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        review = self.get_review()
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(
            author=self.request.user, review=review
        )


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ['username']
    permission_classes = [AdminOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['patch', 'get'],
        permission_classes=[AdminOnly | IsAuthenticated],
        detail=False,
        url_path=MEUSERNAME,
        url_name=MEUSERNAME
    )
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            if 'role' in request.data:
                return Response(
                    'Нельзя менять свою роль!'
                    'Изменение поля role доступно только'
                    'администраторам и модераторам',
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)
