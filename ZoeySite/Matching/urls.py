from django.conf.urls import url
from django.contrib import admin
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .views import ActiveListView

app_name = 'Matching'

urlpatterns = [
    path('active/', ActiveListView.as_view(), name='active_list'),
]
