from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.db.models import JSONField
from django.utils import timezone


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=20)
    age = models.IntegerField(blank=True)
    interests = JSONField(blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(verbose_name="active", default=True)
    is_superuser = models.BooleanField(verbose_name="superuser", default=False)
    is_staff = models.BooleanField(verbose_name="staff", default=False)
    is_online = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Chat(models.Model):
    chat_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_sender")
    chat_recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_recipient")


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat")
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_sender")
    message_recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_recipient")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
