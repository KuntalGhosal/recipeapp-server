from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from decouple import config



@shared_task(bind=True)
def send_mail_func(self,user):
    mail_subject="You have new like on recipe"
    message="Testing mail through celery"
    to_mail=user
    from_mail=config('EMAIL_USER')
    send_mail(
        subject=mail_subject,
        message=message,
        from_email= from_mail,
        recipient_list=[to_mail],
        fail_silently=True
    )
    
    return "DONE"