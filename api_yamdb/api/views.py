from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin,
)

from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReadTitleSerializer
)
from .permissions import IsAdmin, IsModerator, IsAuthor, PutError


# class GenrePagination(PageNumberPagination):
#    page_size = 10  # Установите нужное количество объектов на странице


User = get_user_model()


class CategoryViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    """ViewSet для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)


class GenreViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    """ViewSet для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений (Title)."""
    permission_classes = [IsAdmin]

    def get_queryset(self):
        queryset = Title.objects.all()
        category = self.request.query_params.get('category')
        genre = self.request.query_params.get('genre')
        name = self.request.query_params.get('name')
        year = self.request.query_params.get('year')
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        if year is not None:
            queryset = queryset.filter(year=year)
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadTitleSerializer
        return TitleSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return (AllowAny(),)
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        if self.request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return super().update(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        title = self.get_title()
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(
            author=self.request.user, title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]

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

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями."""
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ['username']
    permission_classes = [IsAdmin | IsAuthenticated]

    @action(detail=False, methods=['patch'], url_path='me', permission_classes=[IsAuthenticated])
    def update_me(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
