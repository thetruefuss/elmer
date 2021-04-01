#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Profile


class TestProfileModel(TestCase):
    """
    TestCase class to test the profile model functionality
    """
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user',
                                                    email='test@gmail.com',
                                                    password='top_secret')
        self.other_user = get_user_model().objects.create(username='other_test_user',
                                                          email='other_test@gmail.com',
                                                          password='top_secret')
        self.profile = Profile.objects.get(user=self.user, )
        self.profile_two = Profile.objects.get(user=self.other_user, )
        self.profile.dob = '2002-12-12'
        self.profile.save()

    def test_object_instance(self):
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertTrue(isinstance(self.profile_two, Profile))
        self.assertTrue(isinstance(self.profile.user, User))

    def test_return_screen_name(self):
        self.assertEqual(self.profile.screen_name(), self.user.username)

    def test_return_str(self):
        self.assertEqual(str(self.profile), 'test_user')


class TestRegisterViews(TestCase):
    """
    Includes tests for all the functionality
    associated with register_user Views
    """
    def setUp(self):
        self.client = Client()
        self.other_client = Client()
        self.user = get_user_model().objects.create(username='test_user',
                                                    email='test@gmail.com',
                                                    password='top_secret')
        self.other_user = get_user_model().objects.create(username='other_test_user',
                                                          email='other_test@gmail.com',
                                                          password='top_secret')
        self.client.login(username='test_user', password='top_secret')
        self.other_client.login(username='other_test_user', password='top_secret')

    def test_post_empty_response(self):
        response = self.client.post(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_alternate_empty_response(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
