from django.urls import reverse, resolve
from django.test import TestCase
from .views import home, topic_list, new_topic
from .models import Board, Topic, Post
from django.conf import settings


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

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('Board:topic_list', kwargs={'pk': 1})
        homepage_url = reverse('Board:home')
        new_topic_url = reverse('Board:new_topic', kwargs={'pk': 1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))


# contents.htmlのテスト
class TopicListTests(TestCase):
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


# new_topic.htmlの検証
class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        settings.AUTH_USER_MODEL.objects.create_user(username='john', email='john@doe.com', password='123')

    def test_new_topic_view_success_status_code(self):
        url = reverse('Board:new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('Board:new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('Board:new_topic', kwargs={'pk': 1})
        board_topics_url = reverse('Board:board_list', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):
        url = reverse('Board:new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('Board:new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        """Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """
        url = reverse('Board:new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        """
       Invalid post data should not redirect
       The expected behavior is to show the form again with validation errors
       """
        url = reverse('Board:new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

