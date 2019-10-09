from django.contrib import admin
from .models import Tag, Topic, Post
from markdownx.admin import MarkdownxModelAdmin


# Register your models here.
admin.site.register(Tag)
admin.site.register(Topic, MarkdownxModelAdmin)
admin.site.register(Post)
