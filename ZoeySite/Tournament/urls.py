from django.urls import path, reverse_lazy
from .views import TournamentListView, TournamentDetailView, TournamentCreateView
app_name = 'Tournament'

urlpatterns = [
    path('', TournamentListView.as_view(), name='tournament_list'),
    path('<int:pk>/', TournamentDetailView.as_view(), name='tournament_detail'),
    path('create/', TournamentCreateView.as_view(), name='tournament_create'),
]
