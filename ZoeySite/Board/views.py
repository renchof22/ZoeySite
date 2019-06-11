from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Board, Topic, Post
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import NewTopicForm


def home(request):
    boards = Board.objects.all()
    return render(request, 'Board/home.html', {'boards': boards})


def topic_list(request, pk):
    """ページが存在しない場合は404エラー"""
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'Board/topic_list.html', {'board': board})


def new_topic(request, pk):
    """新しくトピックを作成する"""
    board = get_object_or_404(Board, pk=pk)
    user = request.user

    # Postメソッドの場合
    if request.method == 'POST':
        form = NewTopicForm(request.POST)   # 送信データインスタンス作成
        # データのバリデーション実行
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                posted_by=user
            )
            # TODO : redirect to top page
            return redirect('Board:topic_list', pk=board.pk)
    else:
        form = NewTopicForm()

    return render(request, 'Board/new_topic.html', {'board': board, 'form': form})
