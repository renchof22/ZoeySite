from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import (
    LoginForm,
    SignUpForm,
)
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
# User = get_user_model()


# ユーザー登録ページ
def signup(request):
    # Submitボタンを押したら
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        # 入力内容に問題がなければ
        if form.is_valid():
            user = form.save()          # ユーザ情報保存
            auth_login(request, user)   # ログイン
            return redirect('index')    # リダイレクト
    else:
        form = SignUpForm()

    context = {
        'form': form,
    }
    return render(request, 'Accounts/signup.html', context)


# ログインページ
def login(request):
    context = {
        'template_name': 'login.html',
        'authentication_form': LoginForm
    }
    return auth_views.LoginView(request, **context)


# ログアウトページ
def logout(request):
    context = {
        'template_name': 'index.html',
    }
    return auth_views.LogoutView(request, **context)


@require_POST
def regist_save(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('users:index')

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)
