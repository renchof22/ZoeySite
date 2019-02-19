from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'Accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="Accounts/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="index.html"), name='logout'),
]
