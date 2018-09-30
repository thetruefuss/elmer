from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, authenticate, login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.generic import ListView

import requests

from mysite.decorators import ajax_required
from notifications.models import Notification
from subjects.models import Subject
from utils import check_image_extension

from .forms import ProfileEditForm, SignupForm, UserEditForm
from .models import Profile


def register_user(request):
    """
    Displays a sign up form and handles signup action.
    """
    form_filling = True

    if request.method == 'POST':
        user_form = SignupForm(data=request.POST or None)
        if not user_form.is_valid():
            return render(request, 'registration/register.html', {
                'user_form': user_form, 'form_filling': form_filling
            })
        else:
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
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                auth = authenticate(
                    username=user_form.cleaned_data['username'],
                    password=user_form.cleaned_data['password'],
                )
                auth_login(request, auth)

                msg_txt = """
                    <h4 class="alert-heading">
                        Welcome to elmer!
                    </h4>
                    <p>
                        Thanks for joining our community. Start sharing your ideas by posting
                        <a href="/new_post/" class="alert-link">new subject</a> or just create
                        your own <a href="/new_board/" class="alert-link">new board</a>.
                    </p>
                    <hr>
                    <p class="mb-0">
                        Add your <a href="/profile_edit/" class="alert-link">profile info</a>,
                        so community members know you well.
                    </p>
                """

                messages.success(request, msg_txt)
                return redirect('/')
    else:
        user_form = SignupForm()
    return render(request, 'registration/register.html', {
        'user_form': user_form, 'form_filling': form_filling
    })


@ajax_required
def check_username(request):
    """
    Ajax call to check username availability.
    """
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


@login_required
def user_logout(request):
    """
    Logout the current user.
    """
    auth_logout(request)
    return redirect('/')


class UsersPageView(ListView):
    """
    Basic ListView implementation to call the users list.
    """
    model = User
    paginate_by = 20
    template_name = 'users/view_all_users.html'
    context_object_name = 'users'

    def get_queryset(self, **kwargs):
        return User.objects.exclude(username=self.request.user.username)


class FollowersPageView(LoginRequiredMixin, ListView):
    """
    Basic ListView implementation to call the followers list per user.
    """
    model = User
    paginate_by = 20
    template_name = 'users/followers.html'
    context_object_name = 'users'

    def get_queryset(self, **kwargs):
        return self.request.user.profile.followers.all()


class FollowingPageView(LoginRequiredMixin, ListView):
    """
    Basic ListView implementation to call the following list per user.
    """
    model = User
    paginate_by = 20
    template_name = 'users/following.html'
    context_object_name = 'profiles'

    def get_queryset(self, **kwargs):
        return self.request.user.following.all()


@login_required
@ajax_required
def follow_user(request, user_id):
    """
    Ajax call to follow a user.
    """
    user = get_object_or_404(User,
                             id=user_id)
    if request.user in user.profile.followers.all():
        user.profile.followers.remove(request.user)
        text = 'Follow'
    else:
        user.profile.followers.add(request.user)
        Notification.objects.create(
            Actor=request.user,
            Target=user,
            notif_type='follow'
        )
        text = 'Unfollow'
    return HttpResponse(text)


@login_required
def profile_edit(request):
    """
    Handles user profile edit action.
    """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST)
        if user_form.is_valid():
            user_form.save()
        else:
            user_form = UserEditForm(instance=request.user)

        if profile_form.is_valid():
            profile_form.save()
        else:
            profile_form = ProfileEditForm(instance=request.user.profile)

        msg_txt = """
            <p>Your profile info is successfully saved. <a href="/" class="alert-link">Go to homepage</a></p>
        """

        messages.success(request, msg_txt)
        return redirect('profile_edit')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'users/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def change_picture(request):
    """
    Handles profile picture change action.
    """
    if request.method == 'POST':
        user_dp = request.FILES.get('dp')
        if check_image_extension(user_dp.name):
            profile_form = Profile.objects.get(user=request.user)
            profile_form.dp = user_dp
            profile_form.save()
            msg_txt = """
                <p>Your profile picture is successfully saved. <a href="/" class="alert-link">Go to homepage</a></p>
            """
            messages.success(request, msg_txt)
        else:
            msg_txt = """
                <p>
                    Filetype not supported. Please use .jpg or .png filetypes.
                    <a href="/" class="alert-link">Go to homepage</a>
                </p>
            """
            messages.warning(request, msg_txt)
            return redirect('picture_change')

        return redirect('user_profile', username=request.user.username)
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'users/change_picture.html', {'profile_form': profile_form})


class UserProfilePageView(LoginRequiredMixin, ListView):
    """
    Basic ListView implementation to call the subjects list & profile per user.
    """
    model = Subject
    paginate_by = 15
    template_name = 'users/profile.html'
    context_object_name = 'subjects'

    def get_queryset(self, **kwargs):
        self.user = get_object_or_404(User,
                                      username=self.kwargs['username'])
        return Subject.get_subjects(self.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["user"] = self.user
        return context


@login_required
@ajax_required
def send_message_request(request, user_id):
    """
    Ajax call to send a message request.
    """
    receiver = get_object_or_404(User, id=user_id)
    contacter = request.user

    if contacter in receiver.profile.pending_list.all():
        receiver.profile.pending_list.remove(contacter)
        text = 'Send Request'
    else:
        receiver.profile.pending_list.add(contacter)
        Notification.objects.create(Actor=contacter, Target=receiver, notif_type='sent_msg_request')
        text = 'Request Sent'
    return HttpResponse(text)


@login_required
@ajax_required
def accept_message_request(request, user_id):
    """
    Ajax call to accept a message request.
    """
    sender = get_object_or_404(User, id=user_id)
    acceptor = request.user

    if sender in acceptor.profile.pending_list.all():
        acceptor.profile.pending_list.remove(sender)
        acceptor.profile.contact_list.add(sender)
        sender.profile.contact_list.add(acceptor)
        Notification.objects.create(Actor=acceptor, Target=sender, notif_type='confirmed_msg_request')
        text = 'Added to contact list'
    else:
        text = 'Unexpected error!'
    return HttpResponse(text)


@login_required
def block_spammer(request, user_id):
    """
    Remove user from requester's contact list.
    """
    spammer = get_object_or_404(User, id=user_id)
    blocker = request.user

    if spammer in blocker.profile.contact_list.all():
        blocker.profile.contact_list.remove(spammer)
        spammer.profile.contact_list.remove(blocker)
        return redirect('user_profile', username=spammer)
    else:
        return redirect('/')


@login_required
def all_message_requests(request):
    """
    Displays a message requests list of users.
    """
    message_requests = request.user.profile.pending_list.all()

    paginator = Paginator(message_requests, 20)
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

    return render(request, 'users/view_all_message_requests.html', {
        'users': users,
        'page': page,
        'p': p,
        'p_obj': p_obj
    })


@login_required
def all_friends(request):
    """
    Displays a friends list of users.
    """
    user_contact_list = request.user.profile.contact_list.all()

    paginator = Paginator(user_contact_list, 20)
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

    return render(request, 'users/view_all_contacts.html', {
        'users': users,
        'page': page,
        'p': p,
        'p_obj': p_obj
    })
