from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import m2m_changed
from django.utils import timezone
from django.utils.html import escape

import bleach
from autoslug import AutoSlugField


class Board(models.Model):

    title = models.CharField(max_length=500, unique=True, db_index=True)
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True)
    description = models.TextField(max_length=2000)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)

    admins = models.ManyToManyField(User, related_name='inspected_boards')
    subscribers = models.ManyToManyField(User, related_name='subscribed_boards')
    banned_users = models.ManyToManyField(User, related_name='forbidden_boards')

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('board',
                       args=[self.slug])

    def get_admins(self):
        return self.admins.all()

    def get_picture(self):
        default_picture = settings.STATIC_URL + 'img/cover.png'
        if self.cover:
            return self.cover.url
        else:
            return default_picture

    def recent_posts(self):
        return self.submitted_subjects.filter(created__gte=timezone.now() - timedelta(days=3)).count()


def admins_changed(sender, **kwargs):
    if kwargs['instance'].admins.count() > 3:
        raise ValidationError("You can't assign more than three admins.")
m2m_changed.connect(admins_changed, sender=Board.admins.through)  # noqa: E305


class Subject(models.Model):

    title = models.CharField(max_length=150, db_index=True)
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True)
    body = models.TextField(max_length=5000, blank=True, null=True)
    photo = models.ImageField(upload_to='subject_photos/',
                              verbose_name=u"Add image (optional)",
                              blank=True,
                              null=True)

    author = models.ForeignKey(User, related_name='posted_subjects')
    board = models.ForeignKey(Board, related_name='submitted_subjects')

    points = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='liked_subjects',
                                    blank=True)
    mentioned = models.ManyToManyField(User, related_name='m_in_subjects', blank=True)

    rank_score = models.FloatField(default=0.0)
    active = models.BooleanField(default=True)

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('subject_detail',
                       args=[self.board.slug,
                             self.slug])

    @staticmethod
    def get_subjects():
        subjects = Subject.objects.filter(active=True)
        return subjects

    @staticmethod
    def search_subjects(query, board=None):
        if board:
            search_results = Subject.objects.filter(active=True,
                                                    title__icontains=query,
                                                    board=board)
        else:
            search_results = Subject.objects.filter(active=True,
                                                    title__icontains=query)
        return search_results

    def get_points(self):
        return self.points.count()

    def linkfy_subject(self):
        return bleach.linkify(escape(self.body))

    def set_rank(self):
        GRAVITY = 1.2
        time_delta = timezone.now() - self.created
        subject_hour_age = time_delta.total_seconds()
        subject_points = self.points.count() - 1
        self.rank_score = subject_points / pow((subject_hour_age + 2), GRAVITY)
        self.save()


class Comment(models.Model):

    subject = models.ForeignKey(Subject, related_name='comments')
    commenter = models.ForeignKey(User, related_name='posted_comments')

    body = models.TextField(max_length=2000)
    active = models.BooleanField(default=True)

    reply = models.ForeignKey("Comment",
                              related_name='comment_reply',
                              null=True,
                              blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('created',)

    def __str__(self):
        return self.body


class Report(models.Model):

    reporter = models.ForeignKey(User, related_name='reported', null=True)

    comment = models.ForeignKey(Comment, related_name='comment_reports', blank=True, null=True)
    subject = models.ForeignKey(Subject, related_name='subject_reports', blank=True, null=True)
    board = models.ForeignKey(Board, related_name='board_reports', blank=True, null=True)

    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ('-created',)

    def __str__(self):
        if self.comment:
            return '{} reported a comment.'.format(
                self.reporter.profile.screen_name()
            )
        else:
            return '{} reported a subject entitled \"{}\" posted by \"{}\".'.format(
                self.reporter.profile.screen_name(),
                self.subject, self.subject.author
            )


class FeaturedPost(models.Model):

    title = models.CharField(max_length=120)
    photo = models.ImageField(upload_to='FeaturedPostPhotos/')
    link = models.URLField(max_length=2000, null=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Featured Post'
        verbose_name_plural = 'Featured Posts'
        ordering = ('-created',)

    def __str__(self):
        return self.title
