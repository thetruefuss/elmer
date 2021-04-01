#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render

from boards.models import Board
from subjects.models import Subject


def search(request, board_slug=None):
    """
    Handles search functionality for all subjects or within some board.
    """
    if 'query' in request.GET:
        q = request.GET.get('query', None)
        if not board_slug:
            subjects_list = Subject.search_subjects(q)
            bv = False
            board = False
        else:
            board = get_object_or_404(Board, slug=board_slug)
            subjects_list = Subject.search_subjects(q, board)
            bv = True

        paginator = Paginator(subjects_list, 15)
        page = request.GET.get('page')
        if paginator.num_pages > 1:
            p = True
        else:
            p = False
        try:
            subjects = paginator.page(page)
        except PageNotAnInteger:
            subjects = paginator.page(1)
        except EmptyPage:
            subjects = paginator.page(paginator.num_pages)

        p_obj = subjects

        return render(request, 'search/search_results.html', {
            'page': page,
            'subjects': subjects,
            'p': p,
            'bv': bv,
            'board': board,
            'q': q,
            'p_obj': p_obj
        })
    else:
        return redirect('home')
