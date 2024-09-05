from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from .serializers import UserRegistrateSeriolizer, TokenSerializer
from api_yamdb.constants import BASE_EMAIL

User = get_user_model()


class CreateOrGetTokenUserViewSet(viewsets.ModelViewSet):
    """Вьюсет, создающий пользователя и (или) отправляюший проверочный код."""

    queryset = User.objects.all()
    serializer_class = UserRegistrateSeriolizer
    permission_classes = (AllowAny,)

    def get_permissions(self):
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        def send_on_email(user, confirmation_code):
            user.confirmation_code = confirmation_code
            user.save()
            send_mail(
                subject='Код подтверждения.',
                message=f'Код подтверждения: {user.confirmation_code}',
                from_email=BASE_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        username = request.data.get('username')
        email = request.data.get('email')
        user = User.objects.filter(username=username).first()
        mail = User.objects.filter(email=email).first()
        if user is None or mail is None:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            confirmation_code = default_token_generator.make_token(user)
            send_on_email(user, confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            confirmation_code = default_token_generator.make_token(user)
            send_on_email(user, confirmation_code)
            return Response(
                {'detail': 'Новый проверочный код был отправлен на почту.'},
                status=status.HTTP_200_OK
            )


class GetJWTTokenView(viewsets.ModelViewSet):
    """ Вью сет, отправляющий JWT токен."""

    permission_classes = (AllowAny,)

    def get_token(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        access = RefreshToken.for_user(user).access_token

        return Response({
            # 'refresh': str(refresh),
            'token': str(access),
        }, status=status.HTTP_200_OK)
