from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Board, Topic, Post
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import NewTopicForm
from django.views import generic
from django.views.generic.edit import ModelFormMixin, ProcessFormView, FormMixin


def home(request):
    boards = Board.objects.all()
    return render(request, 'Board/home.html', {'boards': boards})


class TopicListView(ProcessFormView, generic.ListView):
    """トピック一覧を表示するビュー"""
    model = Topic           # モデル指定
    paginate_by = 10         # 一ページに出力する件数指定
    context_object_name = "topic_list"     # html内でtopic_listという名前で使えるようにする
    template_name = "Board/topic_list.html"
    ordering = ['last_updated']

    # def get_context_data(self, *args, **kwargs):
    #     """htmlコンテキストへdictを渡す"""
    #     context = super(ActiveListView, self).get_context_data(*args, **kwargs)
    #     context['form'] = CommentForm()
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     """POSTメソッドの際に呼び出される関数"""
    #     self.object = None
    #     self.object_list = self.get_queryset()
    #     form = CommentForm(request.POST)
    #     # commit = FalseでFormに適したモデルインスタンスを作成する。この場合はMatchingモデルインスタンス
    #     comment = form.save(commit=False)
    #     # senderとmatchingはhtmlで指定しない。formで指定するとエラー
    #     comment.sender = request.user
    #     comment.matching = get_object_or_404(Matching, pk=request.POST["matching_id"])
    #
    #     if form.is_valid():
    #         comment.save()
    #         return redirect('Matching:active_list')
    #     else:
    #         return redirect('Matching:active_list')
    #
    def get(self, request, *args, **kwargs):
        """GETメソッドで呼ばれる関数"""
        self.object = None
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)


class TopicDetailView(generic.DetailView):
    """トピックの詳細を表示するビュー"""
    template_name = "Board/topic_detail.html"
    model = Topic
    context_object_name = "topic_instance"

    def get_context_data(self, **kwargs):
        """HTMLファイルに変数を渡す関数。Get毎に呼ばれるっぽい"""
        context = super().get_context_data(**kwargs)
        # TODO:ここがエラー
        post_list = Post.objects.filter(topic=self.object)
        context['post_list'] = post_list
        return context


def topic_list(request):
    """ページが存在しない場合は404エラー"""
    topic = get_object_or_404(Topic, pk=pk)
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
