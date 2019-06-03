from django.http import HttpResponse
from django.shortcuts import render
from .models import Board
from django.shortcuts import render, get_object_or_404


def home(request):
    boards = Board.objects.all()
    return render(request, 'Board/home.html', {'boards': boards})


def topic_list(request, pk):
    """ページが存在しない場合は404エラー"""
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'Board/topic_list.html', {'board': board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'Board/new_topic.html', {'board': board})
