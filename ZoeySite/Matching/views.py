from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Matching


def active_list(request):
    """現在アクティブなUSERを取得して表示"""
    matching = Matching.objects.all()
    return render(request, 'Matching/active_list.html', {'matching': matching})
