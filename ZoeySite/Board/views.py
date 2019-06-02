from django.http import HttpResponse
from django.shortcuts import render
from .models import Board
from django.shortcuts import render, get_object_or_404


def home(request):
    boards = Board.objects.all()
    return render(request, 'Board/home.html', {'boards': boards})


def contents(request, pk):
    """ページが存在しない場合は404エラー"""
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'Board/contents.html', {'board': board})
