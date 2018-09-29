from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models
from django.db.models.signals import m2m_changed
from django.utils import timezone

from slugify import UniqueSlugify


class Board(models.Model):
    """
    Model that represents a board.
    """
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500)
    cover = models.ImageField(
        upload_to='board_covers/', blank=True, null=True
    )
    admins = models.ManyToManyField(User, related_name='inspected_boards')
    subscribers = models.ManyToManyField(User, related_name='subscribed_boards')
    banned_users = models.ManyToManyField(User, related_name='forbidden_boards')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        """Unicode representation for a board model."""
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = board_slugify(f"{self.title}")

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for a board."""
        return reverse('board',
                       args=[self.slug])

    def get_admins(self):
        """Return admins of a board."""
        return self.admins.all()

    def get_picture(self):
        """Return cover url (if any) of a board."""
        default_picture = settings.STATIC_URL + 'img/cover.png'
        if self.cover:
            return self.cover.url
        else:
            return default_picture

    def recent_posts(self):
        """
        Counts number of posts posted within last 3 days in a board.
        """
        return self.submitted_subjects.filter(created__gte=timezone.now() - timedelta(days=3)).count()


def admins_changed(sender, **kwargs):
    """
    Signals the Board to not assign more than 3 admins to a board.
    """
    if kwargs['instance'].admins.count() > 3:
        raise ValidationError("You can't assign more than three admins.")
m2m_changed.connect(admins_changed, sender=Board.admins.through)  # noqa: E305


def board_unique_check(text, uids):
    if text in uids:
        return False
    return not Board.objects.filter(slug=text).exists()


board_slugify = UniqueSlugify(
                    unique_check=board_unique_check,
                    to_lower=True,
                    max_length=80,
                    separator='_',
                    capitalize=False
                )
