#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Board


class TestBoardsViews(TestCase):
    """
    TestCase class to test the boards views.
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
        # This user will be banned in the `board`.
        self.user_to_ban = get_user_model().objects.create_user(username='user_to_ban',
                                                                email='user_to_ban@gmail.com',
                                                                password='top_secret')
        self.board = Board.objects.create(title='test title 1', description='some random words')
        # Make `user` the admin & subscriber.
        self.board.admins.add(self.user)
        self.board.subscribers.add(self.user)
        # Ban `other_user` from board.
        self.board.banned_users.add(self.other_user)
        self.other_board = Board.objects.create(title='test title 2', description='some random words')

    def test_boards_page_view(self):
        """Test boards list view."""
        response = self.client.get(reverse('view_all_boards'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('boards' in response.context.keys())
        self.assertTrue('test title 1' in str(response.context['boards']))

    def test_banned_users_list(self):
        """Test banned users list view."""
        url = reverse('banned_users', kwargs={'board': self.board.slug})
        # When admin requests the list.
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('users' in response.context.keys())
        self.assertEqual(len(response.context['users']), 1)
        # When anonymous user requests the list.
        other_response = self.anonymous_client.get(url)
        self.assertRedirects(other_response, other_response.url, status_code=302)

    def test_ban_user_view(self):
        """Test ban user view functionality."""
        response = self.client.get(
            reverse('ban_user', kwargs={
                'board': self.board.slug,
                'user_id': self.user_to_ban.id
            }))
        self.assertRedirects(response, reverse('banned_users', kwargs={'board': self.board.slug}), status_code=302)

    def test_user_subscription_list_view(self):
        """Test the users subscriptions list."""
        response = self.client.get(reverse('user_subscription_list', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('subscriptions' in response.context.keys())
        self.assertEqual(len(response.context['subscriptions']), 1)
        self.assertTrue('test title 1' in str(response.context['subscriptions']))

    def test_user_created_boards_page_view(self):
        """Test boards list created by certain user."""
        response = self.client.get(reverse('user_created_boards', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user_boards' in response.context.keys())
        self.assertEqual(len(response.context['user_boards']), 1)
        self.assertTrue('test title 1' in str(response.context['user_boards']))

    def test_board_page_view(self):
        """Test board page view."""
        # logged in client
        response = self.client.get(reverse('board', kwargs={'board': self.board.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('subjects' in response.context.keys())
        self.assertEqual(len(response.context['subjects']), 0)
        # anonymous client
        other_response = self.anonymous_client.get(reverse('board', kwargs={'board': self.board.slug}))
        self.assertEqual(response.status_code, 200)

    def test_create_board_view(self):
        """Test the creation of boards."""
        # Interent connection is required to make this test pass.
        current_boards_count = Board.objects.count()
        response = self.client.post(reverse('new_board'), {
            'title': 'Not much of a title',
            'description': 'babla',
        })
        self.assertEqual(response.status_code, 302)
        new_board = Board.objects.get(title='Not much of a title')
        self.assertEqual(new_board.title, 'Not much of a title')
        self.assertEqual(Board.objects.count(), current_boards_count + 1)

    def test_subscribe_board(self):
        """Test the subscribed ajax call & response."""
        response = self.other_client.get(reverse('subscribe', kwargs={'board': self.board.slug}),
                                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # `other_user` is banned in previous test so it'll raise PermissionDenied.
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.board.subscribers.count(), 1)

    def test_edit_board_cover_view(self):
        """Test if non admin can edit board cover."""
        response = self.other_client.get(reverse('edit_board_cover', kwargs={'board': self.board.slug}))
        self.assertEqual(response.status_code, 403)

    def test_board_view_success_status_code(self):
        """Test board detail view with right url."""
        response = self.client.get(reverse('board', kwargs={'board': self.board.slug}))
        self.assertEqual(response.status_code, 200)

    def test_board_view_not_found_status_code(self):
        """Test board detail view with wrong url."""
        response = self.client.get(reverse('board', kwargs={'board': 'does-not-exists'}))
        self.assertEqual(response.status_code, 404)
