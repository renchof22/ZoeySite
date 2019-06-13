from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    """ModelFormはMetaのModel=でモデルに対応したフォームを作成してくれる"""
    class Meta:
        # 紐づくモデルを指定する
        model = Message
        # formで入力してもらうfieldを定義する・__all__は使わないのが定石らしい。
        fields = ['bodyText', 'sender', 'receiver']
        # TODO:widgetsとは
        widgets = {'sender': forms.HiddenInput(attrs={'readonly': 'readonly'}),
                   'receiver': forms.HiddenInput(attrs={'readonly': 'readonly'})
                   }
