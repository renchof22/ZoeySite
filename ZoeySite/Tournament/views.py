from django.shortcuts import render
from django.views import generic
from .models import IndividualTournament
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import IndividualTournamentSearchForm, IndividualTournamentCreateForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect


class TournamentListView(LoginRequiredMixin, generic.ListView):
    """トーナメントリストを表示するビュー。検索機能持ち"""
    template_name = "Tournament/tournament_list.html"
    paginate_by = 5
    model = IndividualTournament

    def post(self, request, *args, **kwargs):
        # HTMLからの入力を保持
        form_value = [
            self.request.POST.get('game', None),
        ]
        # 前回の検索条件をセッションに保存
        request.session['form_value'] = form_value
        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        game = ''
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            game = form_value[0]
        default_data = {'game': game, }
        search_form = IndividualTournamentSearchForm(initial=default_data)  # 検索フォーム
        context['search_form'] = search_form
        return context

    def get_queryset(self):
        # sessionに値がある場合、その値でクエリ発行する。
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            game = form_value[0]
            # 検索条件
            condition_game = Q()
            if len(game) != 0 and game[0]:
                condition_game = Q(game__icontains=game)
            return IndividualTournament.objects.select_related().filter(condition_game)
        else:
            # 何も返さない
            return IndividualTournament.objects.none()


class TournamentDetailView(LoginRequiredMixin, generic.DetailView):
    """トーナメントの詳細を表示するビュー"""

    template_name = "Tournament/tournament_detail.html"
    model = IndividualTournament
    context_object_name = "tournament"

    def post(self, request, *args, **kwargs):
        """POSTメソッドの際に呼び出される関数"""
        obj = self.get_object()
        # 参加済みならcancelアクションがHTMLから送られてくる
        if request.POST["user_action"] == "cancel":
            obj.participant.remove(request.user)
        else :
            obj.participant.add(request.user)
        return redirect('Tournament:tournament_list')

    def get_context_data(self, **kwargs):
        """HTMLファイルに変数を渡す関数。Get毎に呼ばれるっぽい"""
        context = super().get_context_data(**kwargs)
        return context


class TournamentCreateView(LoginRequiredMixin, generic.CreateView):
    """大会作成用ビュー"""
    model = IndividualTournament
    form_class = IndividualTournamentCreateForm
    template_name = "Tournament/tournament_create.html"
    success_url = "/"  # 成功時にリダイレクトするURL

    def form_valid(self, form):
        """フォームのバリデーションが通った時の処理"""
        obj = form.save(commit=False)
        obj.organizer = self.request.user
        obj.save()
        return super().form_valid(form)
