#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from boards.models import Board
from subjects.models import Subject

from ..models import Comment


class TestCommentsViews(TestCase):
    """
    TestCase class to test the comments views.
    """
    def setUp(self):
        # This client will be logged in, admin & subscriber of the `board`.
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='test_user',
                                                         email='test@gmail.com',
                                                         password='top_secret')
        self.client.login(username='test_user', password='top_secret')
        # Another logged in client.
        self.other_client = Client()
        self.other_user = get_user_model().objects.create_user(username='other_test_user',
                                                               email='other_test@gmail.com',
                                                               password='top_secret')
        self.other_client.login(username='other_test_user', password='top_secret')
        # Anonymous client.
        self.anonymous_client = Client()

        self.board = Board.objects.create(title='test title', description='some random words')
        # Make `user` the admin & subscriber.
        self.board.admins.add(self.user)
        self.board.subscribers.add(self.user)

        self.subject = Subject.objects.create(title='test title',
                                              body='some random words',
                                              author=self.user,
                                              board=self.board)
        self.comment = Comment.objects.create(body='some random words',
                                              commenter=self.other_user,
                                              subject=self.subject)

    def test_deactivate_comment_view(self):
        """Test if admin can deactivate the comment."""
        response = self.client.get(reverse('deactivate_comment', kwargs={'pk': self.comment.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertRedirects(response, response.url, status_code=302)

    def test_delete_comment_view(self):
        """Test if commenter can delete the comment via ajax."""
        url = reverse('delete_comment', kwargs={'pk': self.comment.id})
        # When commenter tries to delete.
        response = self.other_client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)
        # When anonymous user tries to delete.
        other_response = self.anonymous_client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertRedirects(other_response, other_response.url, status_code=302)
