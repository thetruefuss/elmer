from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic import ListView

import requests
from cache_memoize import cache_memoize

from comments.forms import CommentForm
from mysite.decorators import ajax_required
from notifications.models import Notification
from utils import image_compression

from .forms import SubjectForm
from .models import Subject


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
    """
    Basic ListView implementation to call the latest subjects list.
    """
    model = Subject
    queryset = get_home_subjects()
    paginate_by = 15
    template_name = 'subjects/home.html'
    context_object_name = 'subjects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Show Sign Up CTA if user is not logged in.
        context['signup_quote'] = True
        return context


class TrendingPageView(ListView):
    """
    Basic ListView implementation to call the trending subjects list.
    """
    model = Subject
    queryset = get_trending_subjects()
    paginate_by = 15
    template_name = 'subjects/trending.html'
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
                               render_to_string('comments/partial_subject_comments.html',  # noqa: E127
                                                {
                                                    'comment': comment,
                                                    'user': user,
                                                    }))

    return html


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

                        # if first two letters of the word is "u/" then the rest of the word
                        # will be treated as a username

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
                            except:  # noqa: E722
                                pass

                    new_comment_id = new_comment.id
                    html = _html_comments(new_comment_id, board, subject)
                    return HttpResponse(html)

    return render(request, 'subjects/subject.html', {
        'subject': subject,
        'comments': comments,
        'board': board,
        'bv': bv,
        'admins': admins
    })


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


@login_required
def new_subject(request):
    """
    Displays a new subject form and handles creation by validating reCAPTCHA.
    """
    if request.method == 'POST':
        subject_form = SubjectForm(request.POST, request.FILES)
        if subject_form.is_valid():

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

                    # if first two letter of the word is "u/" then the rest of the word
                    # will be treated as a username

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
                        except:  # noqa: E722
                            pass

                if new_subject.photo:
                    image_compression(new_subject.photo.name)

                return redirect(new_subject.get_absolute_url())
        else:
            subject_form = SubjectForm(**{'user': request.user})
    else:
        subject_form = SubjectForm(**{'user': request.user})

    form_filling = True

    return render(request, 'subjects/new_subject.html', {
        'subject_form': subject_form, 'form_filling': form_filling
    })


@login_required
@ajax_required
def like_subject(request, subject):
    """
    Ajax call to like a subject & return status.
    """
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
def delete_subject(request, subject):
    """
    Delete the subjects if requester is the author.
    """
    subject = get_object_or_404(Subject,
                                slug=subject)
    if request.user == subject.author:
        subject.delete()
        return HttpResponse('Subject has been deleted.')
    else:
        return HttpResponse('You can not delete this subject.')


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

    return render(request, 'subjects/edit_subject.html', {
        'subject_form': subject_form, 'form_filling': form_filling
    })
