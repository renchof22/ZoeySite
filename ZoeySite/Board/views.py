from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Tag, Topic, Post
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import TopicForm, PostForm
from django.views import generic
from django.views.generic.edit import ModelFormMixin, ProcessFormView, FormMixin
from django.urls import reverse


# def home(request):
#     boards = Board.objects.all()
#     return render(request, 'Board/home.html', {'boards': boards})


class TopicListView(ProcessFormView, generic.ListView):
    """トピック一覧を表示するビュー"""
    model = Topic           # モデル指定
    paginate_by = 10         # 一ページに出力する件数指定
    context_object_name = "topic_list"     # html内でtopic_listという名前で使えるようにする
    template_name = "Board/topic_list.html"
    ordering = ['last_updated']

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
        # saveする
        update.save()
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