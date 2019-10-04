from django.contrib import admin
from .models import Board, Topic, Post
from markdownx.admin import MarkdownxModelAdmin


# Register your models here.
admin.site.register(Board)
admin.site.register(Topic, MarkdownxModelAdmin)
admin.site.register(Post)
