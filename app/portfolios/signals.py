from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Portfolio
from custom_auth.models import User

@receiver(post_save, sender=User)
def create_user_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_portfolio(sender, instance, **kwargs):
    instance.portfolio.save()
