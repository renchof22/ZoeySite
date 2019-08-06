from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Matching, Comment
from .forms import CommentForm
from django.views import generic
from django.views.generic.edit import ModelFormMixin, ProcessFormView, FormMixin
from django.urls import reverse_lazy


class ActiveListView(ProcessFormView, generic.ListView):
    """データの一覧を表示するhtmlに最適なジェネリックビュー"""
    model = Matching        # モデル指定
    paginate_by = 5         # 一ページに出力する件数指定
    context_object_name = "active_list"     # html内でactive_listという名前で使えるようにする
    template_name = "Matching/active_list.html"
    ordering = ['pk']

    form_class = CommentForm

    def get_context_data(self, *args, **kwargs):
        """htmlコンテキストへdictを渡す"""
        context = super(ActiveListView, self).get_context_data(*args, **kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """POSTメソッドの際に呼び出される関数"""
        self.object = None
        self.object_list = self.get_queryset()
        form = CommentForm(request.POST)
        # commit = FalseでFormに適したモデルインスタンスを作成する。この場合はMatchingモデルインスタンス
        comment = form.save(commit=False)
        # senderとmatchingはhtmlで指定しない。formで指定するとエラー
        comment.sender = request.user
        comment.matching = get_object_or_404(Matching, pk=request.POST["matching_id"])

        if form.is_valid():
            comment.save()
            return redirect('Matching:active_list')
        else:
            return redirect('Matching:active_list')

    def get(self, request, *args, **kwargs):
        """GETメソッドで呼ばれる関数"""
        self.object = None
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)
