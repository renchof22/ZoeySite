from django.conf.urls import url
from django.contrib import admin
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'Accounts'

urlpatterns = [
    path('signup/', views.signup,
         name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name="Accounts/login.html"),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name="index.html"),
        name='logout'),
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='Accounts/password_reset.html',
        email_template_name='Accounts/password_reset_email.html',
        subject_template_name='Accounts/password_reset_subject.txt',
        success_url='done/'),
        name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='Accounts/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='Accounts/password_reset_confirm.html',
        success_url=reverse_lazy('Accounts:password_reset_complete')),
        name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='Accounts/password_reset_complete.html'),
        name='password_reset_complete'),
]
