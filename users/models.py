#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    """
    Model that represents a profile.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    dp = models.ImageField(upload_to='dps/', blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    contact_list = models.ManyToManyField(User, related_name='contacters', blank=True)
    pending_list = models.ManyToManyField(User, related_name='my_pending_requests', blank=True)
    member_since = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-member_since', )

    def __str__(self):
        """Unicode representation for a profile model."""
        return self.user.username

    def screen_name(self):
        """Returns screen name."""
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:  # noqa: E722
            return self.user.username

    def get_picture(self):
        """Returns profile picture url (if any)."""
        default_picture = settings.STATIC_URL + 'img/ditto.jpg'
        if self.dp:
            return self.dp.url
        else:
            return default_picture


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Signals the Profile about User creation.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
