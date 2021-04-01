#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView

import requests
from PIL import Image

from mysite.decorators import ajax_required
from subjects.models import Subject
from utils import check_image_extension

from .decorators import user_is_board_admin, user_is_not_banned_from_board
from .forms import BoardForm
from .models import Board


class BoardsPageView(ListView):
    """
    Basic ListView implementation to call the boards list.
    """
    model = Board
    queryset = Board.objects.all()
    paginate_by = 20
    template_name = 'boards/view_all_boards.html'
    context_object_name = 'boards'


class BoardPageView(ListView):
    """
    Basic ListView implementation to call the subjects list per board.
    """
    model = Subject
    paginate_by = 20
    template_name = 'boards/board.html'
    context_object_name = 'subjects'

    def get_queryset(self, **kwargs):
        self.board = get_object_or_404(Board, slug=self.kwargs['board'])
        return self.board.submitted_subjects.filter(active=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["bv"] = True
        context["admins"] = self.board.admins.all()
        context["board"] = self.board
        return context


class UserSubscriptionListView(LoginRequiredMixin, ListView):
    """
    Basic ListView implementation to call the subscriptions list per user.
    """
    model = Board
    paginate_by = 10
    template_name = 'boards/user_subscription_list.html'
    context_object_name = 'subscriptions'

    def get_queryset(self, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        return user.subscribed_boards.all()


@login_required
@ajax_required
@user_is_not_banned_from_board
def subscribe(request, board):
    """
    Subscribes a board & returns subscribers count.
    """
    board = get_object_or_404(Board, slug=board)
    user = request.user
    if board in user.subscribed_boards.all():
        board.subscribers.remove(user)
    else:
        board.subscribers.add(user)
    return HttpResponse(board.subscribers.count())


class UserCreatedBoardsPageView(LoginRequiredMixin, ListView):
    """
    Basic ListView implementation to call the boards list per user.
    """
    model = Board
    paginate_by = 20
    template_name = 'boards/user_created_boards.html'
    context_object_name = 'user_boards'

    def get_queryset(self, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        return user.inspected_boards.all()


@login_required
def new_board(request):
    """
    Displays a form & handle action for creating new board.
    """
    board_form = BoardForm()

    if request.method == 'POST':
        board_form = BoardForm(request.POST, request.FILES)
        if board_form.is_valid():
            new_board = board_form.save()
            new_board.admins.add(request.user)
            new_board.subscribers.add(request.user)
            return redirect(new_board.get_absolute_url())

    form_filling = True

    return render(request, 'boards/new_board.html', {'board_form': board_form, 'form_filling': form_filling})


@login_required
@user_is_board_admin
def edit_board_cover(request, board):
    """
    Displays edit form for board cover and handles edit action.
    """
    board = get_object_or_404(Board, slug=board)
    if request.method == 'POST':
        board_cover = request.FILES.get('cover')
        if check_image_extension(board_cover.name):
            board.cover = board_cover
            board.save()
            return redirect('board', board=board.slug)
        else:
            return HttpResponse('Filetype not supported. Supported filetypes are .jpg, .png etc.')
    else:
        form_filling = True
        return render(request, 'boards/edit_board_cover.html', {'board': board, 'form_filling': form_filling})


@login_required
@user_is_board_admin
def banned_users(request, board):
    """
    Displays a list of banned users to the board admins.
    """
    board = get_object_or_404(Board, slug=board)
    users = board.banned_users.all()

    paginator = Paginator(users, 20)
    page = request.GET.get('page')
    if paginator.num_pages > 1:
        p = True
    else:
        p = False
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    p_obj = users
    bv = True

    return render(request, 'boards/banned_users.html', {
        'board': board,
        'bv': bv,
        'page': page,
        'p_obj': p_obj,
        'p': p,
        'users': users
    })


@login_required
@user_is_board_admin
def ban_user(request, board, user_id):
    """
    Handles requests from board admins to ban users from the board.
    """
    board = get_object_or_404(Board, slug=board)
    user = get_object_or_404(User, id=user_id)
    if board in user.subscribed_boards.all():
        board.subscribers.remove(user)
        board.banned_users.add(user)
        return redirect('banned_users', board=board.slug)
    else:
        board.banned_users.remove(user)
        return redirect('banned_users', board=board.slug)
