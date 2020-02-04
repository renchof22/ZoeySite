from django.conf.urls import url
from django.contrib import admin
from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth import views as auth_views
from . import views as accounts_views

app_name = 'Board'

urlpatterns = [
    path('', TopicIndexView.as_view(), name='topic_index'),
    path('<str:game>/', TopicListView.as_view(), name='topic_list'),
    path('<str:game>/<uuid:pk>/', TopicDetailView.as_view(), name='topic_detail'),
    path('<str:game>/new/', TopicCreateView.as_view(), name='topic_create'),
    path('<str:game>/<uuid:pk>/post/', PostCreateView.as_view(), name='post_create')
]
