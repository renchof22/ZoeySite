from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Matching(models.Model):
    """マッチング用のbooleanを持つモデル。User登録した時点で自動で作成され初期値はFalse"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    reserve_date = models.DateTimeField(auto_now_add=True)
    voice_chat = models.BooleanField(default=False)
    secret_mode = models.BooleanField(default=False)
    PLAY_STYLE_CHOICES = [
        ('エンジョイ', 'エンジョイ'),
        ('ガチ', 'ガチ'),
        ('とりあえず一緒にプレイ', 'とりあえず一緒にプレイ'),
    ]
    play_style = models.CharField(default='エンジョイ', choices=PLAY_STYLE_CHOICES, max_length=20)

    def __str__(self):
        return "<{0}> , <{1}>".format(self.user, self.active)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Matching.objects.create(user=instance)
