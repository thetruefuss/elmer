#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase

from boards.models import Board
from subjects.models import Subject

from ..models import Notification


class TestNotificationsModels(TestCase):
    """
    TestCase class to test the notifications models.
    """
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user',
                                                    email='test@gmail.com',
                                                    password='top_secret')
        self.other_user = get_user_model().objects.create(username='other_test_user',
                                                          email='other_test@gmail.com',
                                                          password='top_secret')
        self.board = Board.objects.create(title='test title', description='some random words')
        self.subject = Subject.objects.create(title='test title',
                                              body='some random words',
                                              author=self.user,
                                              board=self.board)
        self.notification = Notification.objects.create(Actor=self.user,
                                                        Object=self.subject,
                                                        Target=self.other_user,
                                                        notif_type="comment")

    def test_instance_values(self):
        self.assertTrue(isinstance(self.notification, Notification))

    def test_notification_return_value(self):
        self.assertEqual(str(self.notification),
                         '{} commented on your subject \"{}\".'.format(self.user.username, self.subject.title))

    def test_notification_list_count(self):
        """Test to count notifications."""
        self.assertEqual(Notification.objects.count(), 1)
