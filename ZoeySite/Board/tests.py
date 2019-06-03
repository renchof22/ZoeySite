from django.urls import reverse, resolve
from django.test import TestCase
from .views import home, topic_list
from .models import Board


# home.htmlのテスト
class HomeTests(TestCase):

    def setUp(self):
        """疑似的にデータ生成"""
        self.board = Board.objects.create(name='HomeTest', description='HomeTest description.')
        url = reverse('Board:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        """boardのレスポンスのステータスコードが200 OKであるか検証"""
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        """/boards/ではviews.homeが呼び出さられることを検証"""
        """resolve()はURLからビューに変換する関数"""
        view = resolve('/boards/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        """href="/boards/1/"が含まれてるか検証"""
        board_topics_url = reverse('Board:topic_list', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_contents_url = reverse('Board:topic_list', kwargs={'pk': 1})
        response = self.client.get(board_contents_url)
        homepage_url = reverse('Board:home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))


# contents.htmlのテスト
class ContentsTests(TestCase):
    def setUp(self):
        """疑似的にモデルを生成する"""
        Board.objects.create(name='TestName', description='Test description.')

    def test_board_topics_view_success_status_code(self):
        """pk=1で成功するか検証"""
        url = reverse('Board:topic_list', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        """pk=99では404エラー検証"""
        url = reverse('Board:topic_list', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        """/boards/1ではcontentsが呼び出される検証"""
        view = resolve('/boards/1')
        self.assertEquals(view.func, topic_list)
