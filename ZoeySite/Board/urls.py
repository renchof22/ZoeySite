from django.conf.urls import url
from django.contrib import admin
from django.urls import path, reverse_lazy
from .views import TopicListView
from django.contrib.auth import views as auth_views
from . import views as accounts_views

app_name = 'Board'

urlpatterns = [
    # path('', views.home, name='board_home'),
    path('', TopicListView.as_view(), name='topic_list'),
]
