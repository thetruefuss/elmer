#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from boards.models import Board
from comments.models import Comment
from subjects.models import Subject


class Report(models.Model):
    """
    Model that represents a report.
    """
    reporter = models.ForeignKey(User, related_name='reported', null=True, on_delete=models.SET_NULL)
    comment = models.ForeignKey(Comment,
                                related_name='comment_reports',
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL)
    subject = models.ForeignKey(Subject,
                                related_name='subject_reports',
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL)
    board = models.ForeignKey(Board, related_name='board_reports', blank=True, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        """
        Unicode representation for a report model based on report type check.

        P.S: This model needs to have a CharField with choices [REPORT_TYPES]
             to be selected at the time of report creation.
        """
        if self.comment:
            return '{} reported a comment.'.format(self.reporter.profile.screen_name())
        else:
            return '{} reported a subject entitled \"{}\" posted by \"{}\".'.format(
                self.reporter.profile.screen_name(), self.subject, self.subject.author)

    @staticmethod
    def get_reports(boards_slug=None):
        """Returns a list of reports."""
        if boards_slug:
            reports = Report.objects.filter(active=True, board__slug__icontains=boards_slug)
        else:
            reports = Report.objects.filter(active=True)
        return reports
