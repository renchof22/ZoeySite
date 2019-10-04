from django import forms
from .models import Topic, Post


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('board', 'contents')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']
