from django.db import models
from django.conf import settings
# Create your models here.

GAME_CHOICES = [
    ('Fortnite', 'Fortnite'),
    ('ApexLegends', 'ApexLegends'),
    ('BO4', 'BO4'),
    ('BF5', 'BF5'),
    ('R6S', 'R6S'),
]


class BaseTournament(models.Model):
    """トーナメントクラス。開催者"""
    organizer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    game = models.CharField(default='Fortnite', choices=GAME_CHOICES, max_length=20)
    deadTime = models.DateTimeField(auto_now=False)

    class Mete:
        """abstract=Trueでマイグレーションされてもテーブルは作られない"""
        abstract = True


class IndividualTournament(BaseTournament):
    """個人参加の大会モデル"""
    limitParticipant = models.IntegerField(default=4)
    participant = models.ManyToManyField(settings.AUTH_USER_MODEL)


# TODO:クラン管理アプリの作成後取り掛かる
# class ClanTournament(BaseTournament):
#     """クランが参加する大会モデル"""



