from django.conf.urls import url
from django.contrib import admin
from django.urls import path, reverse_lazy
from .views import TopicListView, TopicDetailView, TopicCreateView, PostCreateView
from django.contrib.auth import views as auth_views
from . import views as accounts_views

app_name = 'Board'

urlpatterns = [
    path('', TopicListView.as_view(), name='topic_list'),
    path('<uuid:pk>/', TopicDetailView.as_view(), name='topic_detail'),
    path('new/', TopicCreateView.as_view(), name='topic_create'),
    path('<uuid:pk>/post/', PostCreateView.as_view(), name='post_create')
]
