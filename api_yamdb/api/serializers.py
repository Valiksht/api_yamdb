from rest_framework import serializers
from reviews.models import Review, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'title', 'text', 'author', 'score', 'pub_date']
        read_only_fields = ['pub_date', 'author']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'review', 'text', 'author', 'pub_date']
        read_only_fields = ['pub_date', 'author']