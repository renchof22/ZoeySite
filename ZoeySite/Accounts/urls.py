from django.conf.urls import url
from django.contrib import admin
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from . import views as accounts_views

app_name = 'Accounts'

urlpatterns = [
    # サインアップページ
    path('signup/', views.signup, name='signup'),
    # ログインページ
    path('login/', auth_views.LoginView.as_view(template_name="Accounts/login.html"), name='login'),
    # ログアウトページ
    path('logout/', auth_views.LogoutView.as_view(template_name="index.html"), name='logout'),
    # マイページ兼ユーザ情報閲覧ページ
    path('<int:pk>/', views.UserDetailView.as_view(), name="user_detail"),
    # ユーザ情報更新ページ
    path('<int:pk>/edit/', views.UserUpdateView.as_view(), name="user_update"),

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
    path('settings/password/', auth_views.PasswordChangeView.as_view(
        template_name='Accounts/password_change.html',
        success_url=reverse_lazy('Accounts:password_change_done')),
        name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='Accounts/password_change_done.html'),
        name='password_change_done'),
]
