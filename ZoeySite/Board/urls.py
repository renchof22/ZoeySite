from django.conf.urls import url
from django.contrib import admin
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from . import views as accounts_views

app_name = 'Board'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.topic_list, name='topic_list'),
    path('<int:pk>/new/', views.new_topic, name='new_topic'),
]
