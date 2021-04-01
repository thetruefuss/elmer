#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from boards.models import Board
from comments.models import Comment
from mysite.decorators import ajax_required
from subjects.models import Subject

from .models import Report


@login_required
@ajax_required
def report_subject(request, subject):
    """
    Handles the reporting of subjects.
    """
    subject = get_object_or_404(Subject, slug=subject)
    board = subject.board
    rep = request.user
    Report.objects.create(reporter=rep, subject=subject, board=board)
    return HttpResponse('Report has been sent to admins.')


@login_required
@ajax_required
def report_comment(request, pk):
    """
    Handles the reporting of comments.
    """
    comment = get_object_or_404(Comment, pk=pk)
    rep = request.user
    board = comment.subject.board
    Report.objects.create(reporter=rep, comment=comment, board=board)
    return redirect('subject_detail', board=board.slug, subject=comment.subject.slug)


@login_required
def show_reports(request, board):
    """
    Displays a list of reports per board.
    """
    board = get_object_or_404(Board, slug=board)
    admins = board.admins.all()
    if request.user in admins:
        reports = board.board_reports.filter(active=True)
        bv = True
        return render(request, 'reports/show_reports.html', {
            'reports': reports,
            'board': board,
            'bv': bv,
            'admins': admins
        })
