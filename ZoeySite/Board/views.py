from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import TopicForm, PostForm, TopicSearchForm
from django.views import generic
from django.views.generic.edit import ModelFormMixin, ProcessFormView, FormMixin
from django.urls import reverse
from django.db.models import Q
from .consts import *


class TopicIndexView(generic.ListView):
    model = Game
    context_object_name = "game_list"
    template_name = "Board/topic_index.html"


class TopicListView(ProcessFormView, generic.ListView):
    """トピック一覧を表示するビュー"""
    model = Topic  # モデル指定
    paginate_by = 10  # 一ページに出力する件数指定
    context_object_name = "topic_list"  # html内でtopic_listという名前で使えるようにする
    template_name = "Board/topic_list.html"

    def get(self, request, *args, **kwargs):
        """GETメソッド時呼び出し関数"""
        # request.session.clear()
        self.object = None
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            POSTメソッド時呼び出し関数（検索条件入力時）
            役割：セッションに検索条件を渡す
        """
        # HTMLからの入力保持
        form_value = [
            # self.request.POST.get('game', None),
            self.request.POST.get('date', None),
            self.request.POST.get('order', None),
        ]
        # 検索条件をセッションに保存
        request.session['form_value'] = form_value
        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
            役割：セッションを読み、検索条件の初期値を設定する
        """
        context = super().get_context_data(**kwargs)
        # game = ''
        date = ''
        order = ''
        # sessionに値がある:既存値をセット（ページングしてもform値変えない）
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            # game = form_value[0]
            date = form_value[0]
            order = form_value[1]
        default_data = {'date': date, 'order': order}
        search_form = TopicSearchForm(initial=default_data)
        context['search_form'] = search_form
        context['game'] = self.kwargs['game']
        return context

    def get_queryset(self):
        """
            役割：セッションの検索条件に応じたクエリセットを発行する
        """
        # sessionに値がある場合、その値でクエリ発行する。
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            # game = form_value[0]
            game = self.kwargs['game']
            date = form_value[0]
            order = form_value[1]
            end, start = get_date_range(date)
            print(start, end)
            # 検索条件
            return Topic.objects.select_related().filter(game__title=game,
                                                         last_updated__range=[start, end]).order_by(order)
        else:
            # 何も返さない
            return Topic.objects.none()


class TopicDetailView(generic.DetailView):
    """トピックの詳細を表示するビュー"""
    template_name = "Board/topic_detail.html"
    model = Topic
    context_object_name = "topic_instance"

    def get_context_data(self, **kwargs):
        """HTMLファイルに変数を渡す関数。Get毎に呼ばれるっぽい"""
        # 同じユーザでview数を増やさない処理
        session_key = 'viewed_topic_{}'.format(self.object.pk)
        if not self.request.session.get(session_key, False):
            self.object.views += 1
            self.object.save()
            self.request.session[session_key] = True
        # Postリストを取得
        post_list = Post.objects.filter(topic=self.object)
        # Tagリストを取得
        tag_list = Tag.objects.filter(topic=self.object)
        kwargs['post_list'] = post_list
        kwargs['tag_list'] = tag_list
        kwargs['game'] = self.kwargs['game']
        return super().get_context_data(**kwargs)


class TopicCreateView(generic.CreateView):
    """新しくトピックを作成するview"""
    template_name = "Board/topic_create.html"
    model = Topic
    form_class = TopicForm
    success_url = "/board"

    def form_valid(self, form):
        # saveはせず、モデルを受け取る
        update = form.save(commit=False)
        # starterを設定
        update.starter = self.request.user
        update.game = Game.objects.get(title=self.kwargs['game'])
        # saveする
        update.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class PostCreateView(generic.CreateView):
    """新しくPostを投稿するview"""
    template_name = "Board/post_create.html"
    model = Post
    form_class = PostForm

    # Post投稿後は、投稿先Topicページへ遷移
    def get_success_url(self):
        return reverse('Board:topic_detail', kwargs={'pk': self.object.topic.id})

    # 親topicとpostユーザを格納して保存
    def form_valid(self, form):
        form.instance.topic = Topic.objects.get(id=self.kwargs['pk'])
        form.instance.posted_by = self.request.user
        return super().form_valid(form)
