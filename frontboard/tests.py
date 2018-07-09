from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

from .views import home, board
from .models import Board

# test for home view
class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolve_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)


# test for board view & model
class BoardTests(TestCase):
    def setUp(self):
        Board.objects.create(
            title='test title',
            description='some random words'
        )

    def test_board_view_success_status_code(self):
        url = reverse('board', kwargs={'board': 'test-title'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_view_not_found_status_code(self):
        url = reverse('board', kwargs={'board': 'does-not-exists'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_url_resolve_board_view(self):
        view = resolve('/b/test-title/')
        self.assertEqual(view.func, board)
