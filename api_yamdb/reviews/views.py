
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from .serializers import UserRegistrateSeriolizer, TokenSerializer
from .permissions import IsAdmin

User = get_user_model()


class CreateOrGetTokenUserViewSet(viewsets.ModelViewSet):
    """Вьюсет, создающий пользователя и (или) отправляюший проверочный код."""

    queryset = User.objects.all()
    serializer_class = UserRegistrateSeriolizer
    permission_classes = (IsAdmin,)

    def create(self, request, *args, **kwargs):
        def send_on_email(confirmation_code):
            user.confirmation_code = confirmation_code
            user.save()
            send_mail(
                subject='Код подтверждения.',
                message=f'Код подтверждения: {user.confirmation_code}',
                from_email='from@example.com',
                recipient_list=[user.email],
                fail_silently=True,
            )

        user, created = User.objects.get_or_create(
            email=request.data.get('email'))
        confirmation_code = default_token_generator.make_token(user)
        if created:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user.save()
            send_on_email(confirmation_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            send_on_email(confirmation_code)
            return Response(
                {'detail': 'Новый проверочный код был отправлен на почту.'},
                status=status.HTTP_201_CREATED
            )


class GetJWTTokenView(viewsets.ModelViewSet):
    """ Вью сет, отправляющий JWT токен."""

    permission_classes = (AllowAny,)

    def get_token(self, request):
        serializer = TokenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        user = serializer.validated_data
        # refresh = RefreshToken.for_user(user)
        access = RefreshToken.for_user(user).access_token

        return Response({
            # 'refresh': str(refresh),
            'token': str(access),
        }, status=status.HTTP_200_OK)
