from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action

from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)
from .permissions import IsAdmin, IsModerator, IsAuthor, PutError

class GenrePagination(PageNumberPagination):
    page_size = 10  # Установите нужное количество объектов на странице

User = get_user_model()

class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly | IsAdmin] 
    

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

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthor | IsAdmin | IsModerator]

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)
    
    def get_queryset(self):
        title = self.get_title()
        new_queryset = Review.objects.filter(title=title)
        # new_queryset = title.review.all()
        return new_queryset
    
    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(
            author=self.request.user, title=title
        )

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor | IsAdmin | IsModerator]


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
