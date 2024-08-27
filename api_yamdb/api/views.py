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
