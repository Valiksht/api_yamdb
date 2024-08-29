<<<<<<< HEAD
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

send_mail(
    subject='Тема письма',          
    message='Текст сообщения',  
    from_email='from@example.com',
    recipient_list=['to@example.com'],
    fail_silently=True,
) 
=======
from rest_framework import viewsets
from reviews.models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
>>>>>>> 5388d1ef67e04d8b9fcf6d39b32b1d952d50a799
