from django.conf import settings
from django.contrib.auth.decorators import login_required
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


@login_required
def banned_users(request, board):
    """
    Displays a list of banned users to the board admins.
    """
    board = get_object_or_404(Board,
                              slug=board)
    admins = board.admins.all()
    if request.user in admins:
        users = board.banned_users.all()
        bv = True

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

        return render(request, 'boards/banned_users.html', {
            'board': board,
            'bv': bv,
            'page': page,
            'p_obj': p_obj,
            'p': p,
            'users': users
        })
    else:
        return redirect('home')


@login_required
def ban_user(request, board, user_id):
    """
    Handles requests from board admins to ban users form the board.
    """
    board = get_object_or_404(Board,
                              slug=board)
    if request.user in board.admins.all():
        user = get_object_or_404(User,
                                 id=user_id)
        if board in user.subscribed_boards.all():
            board.subscribers.remove(user)
            board.banned_users.add(user)
            return redirect('banned_users', board=board.slug)
        else:
            board.banned_users.remove(user)
            return redirect('banned_users', board=board.slug)
    else:
        return redirect('home')


class UserSubscriptionListView(ListView):
    """
    Basic ListView implementation to call the subscriptions list per user.
    """
    model = Board
    paginate_by = 10
    template_name = 'boards/user_subscription_list.html'
    context_object_name = 'subscriptions'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self, **kwargs):
        user = get_object_or_404(User,
                                 username=self.request.user)
        return user.subscribed_boards.all()


class UserCreatedBoardsPageView(ListView):
    """
    Basic ListView implementation to call the boards list per user.
    """
    model = Board
    paginate_by = 20
    template_name = 'boards/user_created_boards.html'
    context_object_name = 'user_boards'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self, **kwargs):
        user = get_object_or_404(User,
                                 username=self.request.user)
        return user.inspected_boards.all()


class BoardPageView(ListView):
    """
    Basic ListView implementation to call the subjects list per board.
    """
    model = Subject
    paginate_by = 20
    template_name = 'boards/board.html'
    context_object_name = 'subjects'

    def get_queryset(self, **kwargs):
        self.board = get_object_or_404(Board,
                                       slug=self.kwargs['board'])
        return self.board.submitted_subjects.filter(active=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["bv"] = True
        context["admins"] = self.board.admins.all()
        context["board"] = self.board
        return context


@login_required
def new_board(request):
    """
    Displays a new board form and handles creation by validating reCAPTCHA.
    """
    board_form = BoardForm()

    if request.method == 'POST':
        board_form = BoardForm(request.POST, request.FILES)
        if board_form.is_valid():

            """ Begin reCAPTCHA validation """
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            """ End reCAPTCHA validation """

            if result['success']:
                new_board = board_form.save()
                first_admin = request.user
                new_board.admins.add(first_admin)
                new_board.subscribers.add(first_admin)
                new_board.save()
                return redirect(new_board.get_absolute_url())
        else:
            board_form = BoardForm()
    else:
        board_form = BoardForm()

    form_filling = True

    return render(request, 'boards/new_board.html', {
        'board_form': board_form, 'form_filling': form_filling
    })


@login_required
@ajax_required
def subscribe(request, board):
    """
    Subscribes a board & returns subscribers count.
    """
    board = get_object_or_404(Board,
                              slug=board)
    user = request.user
    if board in user.subscribed_boards.all():
        board.subscribers.remove(user)
    else:
        board.subscribers.add(user)
    return HttpResponse(board.subscribers.count())


@login_required
def edit_board_cover(request, board):
    """
    Displays edit from for board cover and handles edit action.
    """
    board = get_object_or_404(Board,
                              slug=board)
    admins = board.admins.all()
    if request.user in admins:
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
            return render(request, 'boards/edit_board_cover.html', {
                'board': board, 'form_filling': form_filling
            })
    else:
        return HttpResponse('You can not change the cover of this board unless you are an admin here.')
