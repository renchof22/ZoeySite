from django.db import models
from django.conf import settings


class Message(models.Model):
    """簡易的なメッセージモデル"""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    bodyText = models.CharField(max_length=100)

    def __str__(self):
        return "<{0}> , <{1}> , <{2}>".format(self.sender, self.receiver, self.bodyText)
