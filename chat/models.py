from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid


class Chat(models.Model):
    user_id = models.CharField(max_length=200)
    chat_name = models.CharField(max_length=200)
    messages = models.JSONField(default=list)
    created_date = models.DateTimeField(default=timezone.now)
