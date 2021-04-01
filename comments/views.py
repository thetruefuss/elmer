#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string

from mysite.decorators import ajax_required
from subjects.models import Subject

from .decorators import user_is_comment_owner
from .models import Comment


def _html_comments(comment_id, board, subject):
    """Handles comment postings via ajax."""
    subject = get_object_or_404(Subject, board__slug=board.slug, slug=subject.slug)
    comment = subject.comments.get(id=comment_id)
    user = comment.commenter
    html = ''
    html = '{0}{1}'.format(
        html,
        render_to_string(
            'comments/partial_subject_comments.html',  # noqa: E127
            {
                'comment': comment,
                'user': user,
            }))

    return html


@ajax_required
def load_new_comments(request):
    """
    View that loads new comments on single subject.
    """
    last_comment_id = request.GET.get('last_comment_id')
    board = request.GET.get('board')
    subject = request.GET.get('subject')
    user = request.user

    subject = get_object_or_404(Subject, board__slug=board, slug=subject)
    comments = subject.comments.filter(id__gt=last_comment_id)
    if comments:
        html = ''
        html = '{0}{1}'.format(
            html,
            render_to_string(
                'comments/partial_load_more_comments.html',  # noqa: E127
                {
                    'comments': comments,
                    'user': user,
                }))
        return HttpResponse(html)
    else:
        return HttpResponse('')


@login_required
def deactivate_comment(request, pk):
    """
    Handles requests from board admins to deactivate comments form
    the board if reported.
    """
    comment = get_object_or_404(Comment, pk=pk)
    admins = comment.subject.board.admins.all()
    if request.user in admins:
        reports = comment.comment_reports.all()
        board_reports = comment.subject.board.board_reports.all()

        for report in reports:
            if report in board_reports:
                comment.active = False
                comment.save()
            else:
                return redirect('home')
    else:
        return redirect('home')
    return redirect('home')


@login_required
@ajax_required
@user_is_comment_owner
def delete_comment(request, pk):
    """
    Delete the comment if the requester is the commenter.
    """
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return HttpResponse('This comment has been deleted.')
