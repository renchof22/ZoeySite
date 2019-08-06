from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

from django import forms

from django.contrib.auth import get_user_model
User = get_user_model()


# ユーザー登録用フォーム
# accounts/signup
class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = '＠ユーザー名'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード（確認）'


# ログインフォーム
class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'パスワード'
