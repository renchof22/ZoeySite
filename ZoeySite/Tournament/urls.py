from django.urls import path, reverse_lazy
from .views import TournamentView
app_name = 'Tournament'

urlpatterns = [
    path('', TournamentView.as_view(), name='tournament_list'),
]
