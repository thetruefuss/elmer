#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Board


class TestBoardsModels(TestCase):
    """
    TestCase class to test the boards models.
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test_user',
                                                         email='test@gmail.com',
                                                         password='top_secret')
        self.board = Board.objects.create(title='test title 1', description='some random words')
        # Make `user` the admin & subscriber.
        self.board.admins.add(self.user)
        self.board.subscribers.add(self.user)

        self.other_board = Board.objects.create(title='test title 2', description='some random words')

    def test_instance_values(self):
        """Test board instance values."""
        self.assertTrue(isinstance(self.board, Board))

    def test_board_return_value(self):
        """Test board string return value."""
        self.assertEqual(str(self.board), 'test title 1')

    def test_boards_list_count(self):
        """Test to count boards."""
        self.assertEqual(Board.objects.count(), 2)

    def test_get_admins_method(self):
        """Test get admins method."""
        self.assertEqual(len(self.board.get_admins()), 1)
