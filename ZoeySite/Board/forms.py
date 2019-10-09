from django import forms
from .models import Topic, Post, Tag
from .consts import GAME_LIST

class TopicForm(forms.ModelForm):

    text_tag = forms.CharField(max_length=160, required=False)
    class Meta:
        model = Topic
        fields = ('game', 'contents', 'image', 'tags')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 画像投稿<input>を装飾するため
        self.fields['image'].widget.attrs['style'] = "display:none"

    def save(self, commit=True):
        """
        saveメソッドのオーバーライド
        m2mフィールドを追加・作成するため
        """
        # まず保存
        instance = super(TopicForm, self).save()
        # POSTから受け取ったtext_tagを空白で区切り、既に存在するTagならadd,新規タグならcreate
        split_tags = self.cleaned_data['text_tag'].split()
        for t in split_tags:
            if Tag.objects.filter(tag=t):
                tmp = Tag.objects.get(tag=t)
                instance.tags.add(tmp)
            else:
                instance.tags.create(tag=t)
        return instance

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']
