from django.shortcuts import render
from django.views import generic


# Create your views here.
class TournamentView(generic.TemplateView):
    template_name = "Tournament/tournament_index.html"
