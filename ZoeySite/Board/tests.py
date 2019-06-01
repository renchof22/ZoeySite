from django.urls import reverse, resolve
from django.test import TestCase
from .views import home


# boardのレスポンスのステータスコードが200 OKであるかテスト
class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('Board:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

# resolve()はURLからビューに変換する関数
    def test_home_url_resolves_home_view(self):
        """/boards/ではviews.homeが呼び出さられることを検証"""
        view = resolve('/boards/')
        self.assertEquals(view.func, home)

