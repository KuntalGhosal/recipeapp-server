from django.contrib.auth import get_user_model
from django.db.models import Sum

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from decouple import config

from recipe.models import Recipe



@shared_task(bind=True)
def send_scheduled_mail_func(self):
    users = get_user_model().objects.all()
    mail_subject="Total Likes for Your Delectable Dishes"
    
    
    from_mail=config('EMAIL_USER')
    for user in users:
        to_mail=user.email
        recipe_List = Recipe.objects.filter(author=user)
        total_likes = 3  # Initialize a counter

        # for recipe in recipe_List:
        #     like = recipe_List.aggregate(recipelike=Sum('recipelike__count'))['recipelike'] or 0
            
        message=f"Congratulations on your culinary success! Your recipes have garnered a total of {total_likes} likes from your admirers. Keep up the fantastic work in the kitchen!"
        send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email= from_mail,
                    recipient_list=[to_mail],
                    fail_silently=True
                )    
    
    return "DONE"