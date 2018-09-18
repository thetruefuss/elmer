from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Board


class TestBoardModel(TestCase):
    """
    TestCase class to test the board model functionality
    """
    def setUp(self):
        self.board = Board.objects.create(
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

    def test_instance_values(self):
        self.assertTrue(isinstance(self.board, Board))

    def test_board_return_value(self):
        self.assertEqual(str(self.board), 'test title')
