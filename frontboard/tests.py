from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase

from .models import Board, Comment, Subject
from .views import board, home


class TestHomeView(TestCase):
    """
    TestCase class to test the home view functionality
    """

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolve_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)


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

    def test_board_url_resolve_board_view(self):
        view = resolve('/b/test-title/')
        self.assertEqual(view.func, board)

    def test_instance_values(self):
        self.assertTrue(isinstance(self.board, Board))

    def test_board_return_value(self):
        self.assertEqual(str(self.board), 'test title')


class TestSubjectModel(TestCase):
    """
    TestCase class to test the subject model functionality
    """

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
        )
        self.other_user = get_user_model().objects.create(
            username='other_test_user',
            email='other_test@gmail.com',
            password='top_secret'
        )
        self.board = Board.objects.create(
            title='test title',
            description='some random words'
        )
        self.subject = Subject.objects.create(
            title='test title',
            body='some random words',
            author=self.user,
            board=self.board
        )

    def test_instance_values(self):
        self.assertTrue(isinstance(self.subject, Subject))

    def test_subject_return_value(self):
        self.assertEqual(str(self.subject), 'test title')


class TestCommentModel(TestCase):
    """
    TestCase class to test the comment model functionality
    """

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
        )
        self.other_user = get_user_model().objects.create(
            username='other_test_user',
            email='other_test@gmail.com',
            password='top_secret'
        )
        self.board = Board.objects.create(
            title='test title',
            description='some random words'
        )
        self.subject = Subject.objects.create(
            title='test title',
            body='some random words',
            author=self.user,
            board=self.board
        )
        self.comment = Comment.objects.create(
            body='some random words',
            commenter=self.user,
            subject=self.subject
        )

    def test_instance_values(self):
        self.assertTrue(isinstance(self.comment, Comment))

    def test_comment_return_value(self):
        self.assertEqual(str(self.comment), 'some random words')
