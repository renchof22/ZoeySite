from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.conf import settings
import uuid
from django.contrib.humanize.templatetags.humanize import naturaltime
import re
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from .consts import GAME_LIST

pattern = r"([\,]+),*(.*)"
repeater = re.compile(pattern)

DEFAULT_IMAGE = "../../media/default/no_image.png"

class Tag(models.Model):
    """
    This model associate with Topic.
    User can create and select tag when create Topic.
    """
    tag = models.CharField(max_length=32)

    def __str__(self):
        return "{0}".format(self.tag)


class Topic(models.Model):
    """
    This model is main-contents in Board.
    User create a topic and be reply fro any Users.
    Automatically be added views, reply-count and update-time.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contents = MarkdownxField('Contents')
    last_updated = models.DateTimeField(auto_now_add=True)
    starter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='topics', on_delete=models.SET_NULL, null=True)
    views = models.PositiveIntegerField(default=0)
    game = models.CharField(max_length=32, choices=GAME_LIST, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='topic_images', blank=True, null=True)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(50, 50)],
                                     format='JPEG',
                                     options={'quality': 60})

    objects = models.Manager()

    def __str__(self):
        return "{0}".format(self.id)

    def get_image(self):
        if not self.image:
            return DEFAULT_IMAGE
        else:
            return self.image.url

    def get_image_thumbnail(self):
        if not self.image_thumbnail:
            return DEFAULT_IMAGE
        else:
            return self.image_thumbnail.url

    def get_reply_count(self):
        return self.posts.count()

    def formatted_markdown(self):
        return markdownify(self.contents)

    def get_tags(self):
        return self.tags.all()


class Post(models.Model):
    """
    This models is reply to a Topic.
    """
    message = models.TextField(max_length=1024)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.SET_NULL, null=True)

    objects = models.Manager()

    def __str__(self):
        return "{0},{1},{2}".format(self.topic, self.posted_by, self.message)
