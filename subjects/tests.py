#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase

from boards.models import Board

from .models import Subject


class TestSubjectModel(TestCase):
    """
    TestCase class to test the subject model functionality
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

    def test_instance_values(self):
        self.assertTrue(isinstance(self.subject, Subject))

    def test_subject_return_value(self):
        self.assertEqual(str(self.subject), 'test title')
