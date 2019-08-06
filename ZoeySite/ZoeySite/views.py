from django.shortcuts import render, redirect
from Accounts.forms import LoginForm, SignUpForm
from django.contrib.auth import login as auth_login


# トップページ
def index(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        # 入力内容に問題がなければ
        if form.is_valid():
            user = form.save()  # ユーザ情報保存
            auth_login(request, user)  # ログイン
            return redirect('index')  # TODO:リダイレクト先を変える
    else:
        form = SignUpForm()

    context = {
        'users': request.user,
        'form': form,
    }
    return render(request, 'index.html', context)
