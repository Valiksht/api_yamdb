from django.urls import path

from .views import CreateOrGetTokenUserViewSet, GetJWTTokenView

app_name = 'reviews'


urlpatterns = [
    path(
        'signup/',
        CreateOrGetTokenUserViewSet.as_view({'post': 'create', }),
        name='signup'
    ),
    path(
        'token/',
        GetJWTTokenView.as_view({'post': 'get_token', }),
        name='get_token'
    ),
]
