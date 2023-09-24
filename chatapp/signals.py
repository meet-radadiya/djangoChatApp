from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out

from .redis_cache import update_online_status, update_offline_status


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(user_logged_in)
def online_status_on_login(sender, user, request, **kwargs):
    update_online_status(user)


@receiver(user_logged_out)
def offline_status_on_logout(sender, user, request, **kwargs):
    update_offline_status(user)
