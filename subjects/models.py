from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.utils.html import escape

import bleach
from slugify import UniqueSlugify

from boards.models import Board


class Subject(models.Model):
    """
    Model that represents a subject.
    """
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, null=True, blank=True)
    body = models.TextField(max_length=5000, blank=True, null=True)
    photo = models.ImageField(
        upload_to='subject_photos/', verbose_name=u"Add image (optional)",
        blank=True, null=True
    )
    author = models.ForeignKey(User, related_name='posted_subjects', on_delete=models.CASCADE)
    board = models.ForeignKey(Board, related_name='submitted_subjects', on_delete=models.CASCADE)
    points = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='liked_subjects', blank=True
    )
    mentioned = models.ManyToManyField(
        User, related_name='m_in_subjects', blank=True
    )
    rank_score = models.FloatField(default=0.0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        """Unicode representation for a subject model."""
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = subject_slugify(f"{self.title}")

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for a subject."""
        return reverse('subject_detail',
                       args=[self.board.slug,
                             self.slug])

    @staticmethod
    def get_subjects(user=None):
        """Returns a list of subjects."""
        if user:
            subjects = Subject.objects.filter(active=True,
                                              author=user)
        else:
            subjects = Subject.objects.filter(active=True)
        return subjects

    @staticmethod
    def search_subjects(query, board=None):
        """Searches for subjects."""
        if board:
            search_results = Subject.objects.filter(active=True,
                                                    title__icontains=query,
                                                    board=board)
        else:
            search_results = Subject.objects.filter(active=True,
                                                    title__icontains=query)
        return search_results

    def get_points(self):
        """Returns number of stars."""
        return self.points.count()

    def linkfy_subject(self):
        """Linkifies the subject body."""
        return bleach.linkify(escape(self.body))

    def set_rank(self):
        """Calculates the rank score of a subject."""
        GRAVITY = 1.2
        time_delta = timezone.now() - self.created
        subject_hour_age = time_delta.total_seconds()
        subject_points = self.points.count() - 1
        self.rank_score = subject_points / pow((subject_hour_age + 2), GRAVITY)
        self.save()


def subject_unique_check(text, uids):
    if text in uids:
        return False
    return not Subject.objects.filter(slug=text).exists()


subject_slugify = UniqueSlugify(
                    unique_check=subject_unique_check,
                    to_lower=True,
                    max_length=80,
                    separator='_',
                    capitalize=False
                )
