from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet, CommentViewSet
from .views import TitleViewSet, UserViewSet, ReviewViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='reviews'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('reviews.urls')),
]
