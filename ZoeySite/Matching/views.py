from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Matching
from Messenger.forms import MessageForm


def active_list(request):
    """現在アクティブなUSERを取得して表示"""
    matching = Matching.objects.all()   # TODO:active=ONののみを表示させる
    # Submitボタンを押したら
    if request.method == 'POST':
        # instance = {"sender": request.user, "receiver": request.POST.get("receiver")}
        # instance = request.user
        form = MessageForm(request.POST)

        # 入力内容に問題がなければ
        if form.is_valid():
            message = form.save()  # ユーザ情報保存
            return redirect('index')  # リダイレクト
    else:
        form = MessageForm()

    return render(request, 'Matching/active_list.html', {'matching': matching, 'form': form})
