from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    user = models.ForeignKey(
        User,
        related_name="messages",
        on_delete=models.PROTECT,
    )
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
