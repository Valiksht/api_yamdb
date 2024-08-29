from django.shortcuts import render

# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
# from django.shortcuts import get_object_or_404
# from rest_framework import filters, status, viewsets
# from rest_framework.decorators import action, api_view
# from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import AccessToken

# from api_yamdb import settings

# from .models import User
# from .permissions import IsAdmin
# from .serializers import (ConfirmationCodeSerializer, UserEmailSerializer,
#                           UserSerializer)


# @api_view(['POST'])
# def get_confirmation_code(request):
#     serializer = UserEmailSerializer(data=request.data)

#     serializer.is_valid(raise_exception=True)
#     username = serializer.validated_data.get('username')
#     email = serializer.validated_data.get('email')
#     user, _created = User.objects.get_or_create(username=username, email=email)
#     confirmation_code = default_token_generator.make_token(user)

#     mail_subject = 'Код подтверждения'
#     message = f'Ваш {mail_subject.lower()}: {confirmation_code}'
#     sender_email = settings.DEFAULT_FROM_EMAIL
#     recipient_email = email
#     send_mail(
#         mail_subject,
#         message,
#         sender_email,
#         [recipient_email],
#         fail_silently=False
#     )
#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def get_jwt_token(request):
#     serializer = ConfirmationCodeSerializer(data=request.data)

#     serializer.is_valid(raise_exception=True)
#     email = serializer.validated_data.get('email')
#     confirmation_code = serializer.validated_data.get('confirmation_code')
#     user = get_object_or_404(User, email=email)

#     if default_token_generator.check_token(user, confirmation_code):
#         token = AccessToken.for_user(user).get('jti')
#         return Response({'token': token}, status=status.HTTP_200_OK)

#     resp = {'confirmation_code': 'Неверный код подтверждения'}
#     return Response(resp, status=status.HTTP_400_BAD_REQUEST)


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'username'

#     permission_classes = [IsAdmin | IsAdminUser]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ('user__username',)

#     @action(
#         methods=['patch', 'get'],
#         permission_classes=[IsAuthenticated],
#         detail=False,
#         url_path='me',
#         url_name='me'
#     )
#     def me(self, request, *args, **kwargs):
#         user = self.request.user
#         serializer = self.get_serializer(user)
#         if self.request.method == 'PATCH':
#             serializer = self.get_serializer(
#                 user,
#                 data=request.data,
#                 partial=True
#             )
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#         return Response(serializer.data)