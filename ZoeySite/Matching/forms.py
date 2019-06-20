from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """ModelFormはMetaのModel=でモデルに対応したフォームを作成してくれる"""
    class Meta:
        # 紐づくモデルを指定する
        model = Comment
        # formで入力してもらうfieldを定義する・__all__は使わないのが定石らしい。
        # fields = ['bodyText', 'sender', 'matching']
        fields = ['bodyText']
        # TODO:templatesのincludeを用いてformを表示するとHiddenも表示されてしまうので修正必要
        # widgets = {'sender': forms.HiddenInput(attrs={'readonly': 'readonly'}),
        #            'matching': forms.HiddenInput(attrs={'readonly': 'readonly'})
        #            }
