from django.conf.urls import url
from django.contrib import admin
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from . import views as accounts_views

app_name = 'Board'

urlpatterns = [
    path('', views.board_index, name='board_index'),
]
