from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.conf import settings
import uuid
DEFAULT_IMAGE = "../../media/default/no_image.png"


# 掲示板モデル
class Board(models.Model):
    # 掲示板名
    name = models.CharField(max_length=100)
    # 掲示板概要
    description = models.CharField(max_length=300)
    # 最終書き込み日時
    last_updated = models.DateTimeField(auto_now_add=True)
    # ボード作成者
    creater = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='boards', on_delete=models.SET_NULL, null=True)
    # ボード画像
    image = models.ImageField(upload_to='avatars')
    # ボード画像サムネイル
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(50, 50)],
                                     format='JPEG',
                                     options={'quality': 60})

    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_image(self):
        if not self.image:
            # depending on your template
            return DEFAULT_IMAGE
        else:
            return self.image.url

    def get_image_thumbnail(self):
        if not self.image_thumbnail:
            # depending on your template
            return DEFAULT_IMAGE
        else:
            return self.image_thumbnail.url


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.SET_NULL, null=True)
    starter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='topics', on_delete=models.SET_NULL, null=True)
    # ボード画像
    image = models.ImageField(upload_to='avatars')
    # ボード画像サムネイル
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(50, 50)],
                                     format='JPEG',
                                     options={'quality': 60})
    objects = models.Manager()

    def __str__(self):
        return "{0} , {1}".format(self.id, self.subject)

    def get_image(self):
        if not self.image:
            # depending on your template
            return DEFAULT_IMAGE
        else:
            return self.image.url

    def get_image_thumbnail(self):
        if not self.image_thumbnail:
            # depending on your template
            return DEFAULT_IMAGE
        else:
            return self.image_thumbnail.url


# トピックへの書き込み
class Post(models.Model):
    # 書き込み内容
    message = models.TextField(max_length=4000)
    # 書き込まれた所属ボード
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    # 書き込み日時
    posted_at = models.DateTimeField(auto_now_add=True)
    # 書き込んだUSER
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.SET_NULL, null=True)

    objects = models.Manager()

    def __str__(self):
        return "{0},{1},{2}".format(self.topic.subject, self.posted_by, self.message)
