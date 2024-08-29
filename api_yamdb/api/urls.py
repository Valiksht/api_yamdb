from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet



router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router_v1.urls)),
]



app_name = 'api'

urlpatterns = [
    # path('v1/', ),
]

