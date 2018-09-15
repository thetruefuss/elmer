from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import ListView

import requests
from cache_memoize import cache_memoize
from PIL import Image
from throttle.decorators import throttle
from user_accounts.models import Notification

from mysite.decorators import ajax_required

from .forms import BoardForm, CommentForm, SubjectForm
from .models import Board, Comment, Report, Subject
from .utils import check_image_extension


@cache_memoize(60*15)
def get_trending_subjects():
    subjects = Subject.get_subjects()
    for subject in subjects:
        subject.set_rank()
    return subjects.order_by('-rank_score')


@cache_memoize(60*15)
def get_home_subjects():
    return Subject.get_subjects()


class HomePageView(ListView):
    """Basic ListView implementation to call the latest subjects list."""
    model = Subject
    queryset = get_home_subjects()
    paginate_by = 15
    template_name = 'frontboard/home.html'
    context_object_name = 'subjects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Show Sign Up CTA if user is not logged in.
        context['signup_quote'] = True
        return context


class TrendingPageView(ListView):
    """Basic ListView implementation to call the trending subjects list."""
    model = Subject
    queryset = get_trending_subjects()
    paginate_by = 15
    template_name = 'frontboard/trending.html'
    context_object_name = 'subjects'


def _html_comments(comment_id, board, subject):
    """
    Handles comment postings via ajax.
    """
    subject = get_object_or_404(Subject,
                                board__slug=board.slug,
                                slug=subject.slug)
    comment = subject.comments.get(id=comment_id)
    user = comment.commenter
    html = ''
    html = '{0}{1}'.format(html,
                               render_to_string('frontboard/partial_subject_comments.html',
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

    subject = get_object_or_404(Subject,
                                board__slug=board,
                                slug=subject)
    comments = subject.comments.filter(id__gt=last_comment_id)
    if comments:
        html = ''
        html = '{0}{1}'.format(html,
                                   render_to_string('frontboard/partial_load_more_comments.html',
                                                    {
                                                        'comments': comments,
                                                        'user': user,
                                                        }))
        return HttpResponse(html)
    else:
        return HttpResponse('')


@throttle(zone='default')
def subject_detail(request, board, subject):
    """
    Displays the subject details and handles comment action.
    """
    subject = get_object_or_404(Subject,
                                board__slug=board,
                                slug=subject)
    comments = subject.comments.filter(active=True)
    board = subject.board
    bv = True
    user = request.user
    admins = board.admins.all()

    if request.is_ajax():
        if request.user.is_authenticated():
            if request.method == 'POST':
                comment_form = CommentForm(data=request.POST or None)

                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.commenter = request.user
                    new_comment.subject = subject
                    new_comment.save()

                    if request.user is not subject.author:
                        Notification.objects.create(
                            Actor=new_comment.commenter,
                            Object=new_comment.subject,
                            Target=subject.author,
                            notif_type='comment'
                        )

                    # Checks if someone is mentioned in the comment
                    words = new_comment.body
                    words = words.split(" ")
                    names_list = []
                    for word in words:
                        """
                        if first two letters of the word is "u/" then the rest of the word
                        will be treated as a username
                        """
                        if word[:2] == "u/":
                            u = word[2:]
                            try:
                                user = User.objects.get(username=u)
                                if user not in names_list:
                                    if request.user is not user:
                                        Notification.objects.create(
                                            Actor=new_comment.commenter,
                                            Object=new_comment.subject,
                                            Target=user,
                                            notif_type='comment_mentioned'
                                        )
                                    names_list.append(user)
                            except:
                                pass

                    new_comment_id = new_comment.id
                    html = _html_comments(new_comment_id, board, subject)
                    return HttpResponse(html)

    return render(request, 'frontboard/subject.html', {
        'subject': subject,
        'comments': comments,
        'board': board,
        'bv': bv,
        'admins': admins
    })


class BoardsPageView(ListView):
    """Basic ListView implementation to call the boards list."""
    model = Board
    queryset = Board.objects.all()
    paginate_by = 20
    template_name = 'frontboard/view_all_boards.html'
    context_object_name = 'boards'


@throttle(zone='default')
@login_required
@ajax_required
def report_subject(request, subject):
    """
    Handles the reporting of subjects.
    """
    subject = get_object_or_404(Subject,
                                slug=subject)
    board = subject.board
    rep = request.user
    Report.objects.create(reporter=rep,
                          subject=subject,
                          board=board)
    return HttpResponse('Report has been sent to admins.')


@throttle(zone='default')
@login_required
@ajax_required
def report_comment(request, pk):
    """
    Handles the reporting of comments.
    """
    comment = get_object_or_404(Comment,
                                pk=pk)
    rep = request.user
    board = comment.subject.board
    Report.objects.create(reporter=rep,
                          comment=comment,
                          board=board)
    return redirect('subject_detail', board=board.slug, subject=comment.subject.slug)


@throttle(zone='default')
@login_required
def show_reports(request, board):
    """
    Displays a list of reports per board.
    """
    board = get_object_or_404(Board,
                              slug=board)
    admins = board.admins.all()
    if request.user in admins:
        reports = board.board_reports.filter(active=True)
        bv = True
        return render(request, 'frontboard/show_reports.html', {
            'reports': reports,
            'board': board,
            'bv': bv,
            'admins': admins
        })


@throttle(zone='default')
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

        return render(request, 'frontboard/banned_users.html', {
            'board': board,
            'bv': bv,
            'page': page,
            'p_obj': p_obj,
            'p': p,
            'users': users
        })
    else:
        return redirect('home')


@throttle(zone='default')
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


@throttle(zone='default')
@login_required
def deactivate_subject(request, subject):
    """
    Handles requests from board admins to deactivate subjects form the board if reported.
    """
    subject = get_object_or_404(Subject,
                                slug=subject)
    admins = subject.board.admins.all()
    if request.user in admins:
        reports = subject.subject_reports.all()
        board_reports = subject.board.board_reports.all()

        for report in reports:
            if report in board_reports:
                subject.active = False
                subject.save()
            else:
                return redirect('home')
    else:
        return redirect('home')
    return redirect('home')


@throttle(zone='default')
@login_required
def deactivate_comment(request, pk):
    """
    Handles requests from board admins to deactivate comments form the board if reported.
    """
    comment = get_object_or_404(Comment,
                                pk=pk)
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


class UserSubscriptionListView(ListView):
    """Basic ListView implementation to call the subscriptions list per user."""
    model = Board
    paginate_by = 10
    template_name = 'frontboard/user_subscription_list.html'
    context_object_name = 'subscriptions'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self, **kwargs):
        user = get_object_or_404(User,
                                 username=self.request.user)
        return user.subscribed_boards.all()


class UserCreatedBoardsPageView(ListView):
    """Basic ListView implementation to call the boards list per user."""
    model = Board
    paginate_by = 20
    template_name = 'frontboard/user_created_boards.html'
    context_object_name = 'user_boards'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self, **kwargs):
        user = get_object_or_404(User,
                                 username=self.request.user)
        return user.inspected_boards.all()


class BoardPageView(ListView):
    """Basic ListView implementation to call the subjects list per board."""
    model = Subject
    paginate_by = 20
    template_name = 'frontboard/board.html'
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


def image_compression(f):
    try:
        f = settings.MEDIA_ROOT + f
        im = Image.open(f)
        im.save(f, optimize=True, quality=30)
    except:
        return ""


@throttle(zone='strict')
@login_required
def new_subject(request):
    """
    Displays a new subject form and handles creation by validating reCAPTCHA.
    """
    if request.method == 'POST':
        subject_form = SubjectForm(request.POST, request.FILES)
        if subject_form.is_valid():

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''

            if result['success']:
                new_subject = subject_form.save(commit=False)
                author = request.user
                new_subject.author = author
                new_subject.save()
                new_subject.points.add(author)
                new_subject.save()

                # Checks if someone is mentioned in the subject
                words = new_subject.title + ' ' + new_subject.body
                words = words.split(" ")
                names_list = []
                for word in words:
                    """
                    if first two letter of the word is "u/" then the rest of the word
                    will be treated as a username
                    """
                    if word[:2] == "u/":
                        u = word[2:]
                        try:
                            user = User.objects.get(username=u)
                            if user not in names_list:
                                new_subject.mentioned.add(user)
                                if request.user is not user:
                                    Notification.objects.create(
                                        Actor=new_subject.author,
                                        Object=new_subject,
                                        Target=user,
                                        notif_type='subject_mentioned'
                                    )
                                names_list.append(user)
                        except:
                            pass

                if new_subject.photo:
                    image_compression(new_subject.photo.name)

                return redirect(new_subject.get_absolute_url())
        else:
            subject_form = SubjectForm(**{'user': request.user})
    else:
        subject_form = SubjectForm(**{'user': request.user})

    form_filling = True

    return render(request, 'frontboard/new_subject.html', {
        'subject_form': subject_form, 'form_filling': form_filling
    })


@throttle(zone='default')
@login_required
def new_board(request):
    """
    Displays a new board form and handles creation by validating reCAPTCHA.
    """
    board_form = BoardForm()

    if request.method == 'POST':
        board_form = BoardForm(request.POST, request.FILES)
        if board_form.is_valid():

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''

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

    return render(request, 'frontboard/new_board.html', {
        'board_form': board_form, 'form_filling': form_filling
    })


@login_required
@ajax_required
def like_subject(request, subject):
    data = dict()
    subject = get_object_or_404(Subject,
                                slug=subject)
    user = request.user
    if subject in user.liked_subjects.all():
        subject.points.remove(user)
        data['is_starred'] = False
    else:
        subject.points.add(user)
        data['is_starred'] = True

    data['total_points'] = subject.points.count()
    return JsonResponse(data)


@login_required
@ajax_required
def subscribe(request, board):
    board = get_object_or_404(Board,
                              slug=board)
    user = request.user
    if board in user.subscribed_boards.all():
        board.subscribers.remove(user)
    else:
        board.subscribers.add(user)
    return HttpResponse(board.subscribers.count())


@throttle(zone='default')
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
            board = get_object_or_404(Board,
                                      slug=board_slug)
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

        return render(request, 'frontboard/search.html', {
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


@throttle(zone='default')
@login_required
@ajax_required
def delete_subject(request, subject):
    subject = get_object_or_404(Subject,
                                slug=subject)
    if request.user == subject.author:
        subject.delete()
        return HttpResponse('Subject has been deleted.')
    else:
        return HttpResponse('You can not delete this subject.')


@throttle(zone='default')
@login_required
@ajax_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment,
                                pk=pk)
    if request.user == comment.commenter:
        comment.delete()
        return HttpResponse('This comment has been deleted.')
    else:
        return HttpResponse('You are unable to delete this comment.')


@throttle(zone='strict')
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
                return HttpResponse('filetype not supported. supported filetypes are .jpg,.png')
        else:
            form_filling = True
            return render(request, 'frontboard/edit_board_cover.html', {
                'board': board, 'form_filling': form_filling
            })
    else:
        return HttpResponse('You can not change the cover of this board unless you are an admin here.')


@throttle(zone='default')
@login_required
def edit_subject(request, subject):
    """
    Displays edit from for subjects and handles edit action.
    """
    subject = get_object_or_404(Subject,
                                slug=subject)

    if request.method == 'POST':
        if request.user == subject.author:
            subject_form = SubjectForm(instance=subject,
                                       data=request.POST,
                                       files=request.FILES)

            if subject_form.is_valid():
                subject_form.save()
                return redirect(subject.get_absolute_url())
            else:
                subject_form = SubjectForm(instance=subject)
        else:
            return redirect('/')
    else:
        subject_form = SubjectForm(instance=subject)

    form_filling = True

    return render(request, 'frontboard/edit_subject.html', {
        'subject_form': subject_form, 'form_filling': form_filling
    })
