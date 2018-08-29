from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url, urlsafe_base64_decode

import requests
from frontboard.utils import check_image_extension
from frontboard.models import Subject
from throttle.decorators import throttle

from mysite.decorators import ajax_required

from .forms import ProfileEditForm, SignupForm, UserEditForm
from .models import Profile, Notification


@throttle(zone='full_strict')
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
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                auth = authenticate(
                    username=user_form.cleaned_data['username'],
                    password=user_form.cleaned_data['password'],
                )
                auth_login(request, auth)

                msg_txt = """
                    <h4 class="alert-heading">Welcome to elmer!</h4>
                    <p>Thanks for joining our community. Start sharing your ideas by posting <a href="/new_post/" class="alert-link">new subject</a> or just create your own <a href="/new_board/" class="alert-link">new board</a>.</p>
                    <hr>
                    <p class="mb-0">Add your <a href="/profile_edit/" class="alert-link">profile info</a>, so community members know you well.</p>
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
    wanted_username = request.GET.get('wanted_username', '')
    user_already_exists = User.objects.filter(username=wanted_username).exists()
    if not user_already_exists:
        return HttpResponse('good')
    else:
        return HttpResponse('bad')


def user_login(request, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = AuthenticationForm(request)

    form_filling = True
    context = {
        'form': form,
        'form_filling': form_filling
    }
    return TemplateResponse(request, 'registration/login.html', context)


@throttle(zone='default')
@login_required
def user_logout(request):
    auth_logout(request)
    return redirect('/')


@throttle(zone='default')
def view_all_users(request):
    """
    Displays a list of all the users.
    """
    all_users = User.objects.exclude(username=request.user.username)

    paginator = Paginator(all_users, 20)
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

    return render(request, 'user_accounts/view_all_users.html', {
        'users': users,
        'page': page,
        'p': p,
        'p_obj': p_obj
    })


@throttle(zone='default')
@login_required
def view_all_followers(request):
    """
    Displays a followers list of users.
    """
    all_followers = request.user.profile.followers.all()

    paginator = Paginator(all_followers, 20)
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

    return render(request, 'user_accounts/followers.html', {
        'users': users,
        'page': page,
        'p': p,
        'p_obj': p_obj
    })


@throttle(zone='default')
@login_required
def view_following(request):
    """
    Displays a following list of users.
    """
    all_following = request.user.following.all()

    paginator = Paginator(all_following, 20)
    page = request.GET.get('page')
    if paginator.num_pages > 1:
        p = True
    else:
        p = False
    try:
        profiles = paginator.page(page)

    except PageNotAnInteger:
        profiles = paginator.page(1)

    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    p_obj = profiles

    return render(request, 'user_accounts/following.html', {
        'profiles': profiles,
        'page': page,
        'p': p,
        'p_obj': p_obj
    })


@login_required
@ajax_required
def follow_user(request, user_id):
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


@throttle(zone='default')
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

    return render(request, 'user_accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@throttle(zone='strict')
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
                <p>Filetype not supported. Please use .jpg or .png filetypes. <a href="/" class="alert-link">Go to homepage</a></p>
            """
            messages.warning(request, msg_txt)
            return redirect('picture_change')

        return redirect('user_profile', username=request.user.username)
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'user_accounts/change_picture.html', {'profile_form': profile_form})


@throttle(zone='default')
@login_required
def user_profile(request, username):
    """
    Displays a user profile and submitted subjects list.
    """
    user = get_object_or_404(User,
                             username=username)
    posted_subjects = Subject.get_subjects(user)

    paginator = Paginator(posted_subjects, 15)
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

    return render(request, 'user_accounts/profile.html', {
        'subjects': subjects,
        'user': user,
        'page': page,
        'p': p,
        'p_obj': p_obj
    })


@throttle(zone='default')
@login_required
def activities(request):
    """
    Displays a activities list of users.
    """
    subject_events = Notification.objects.filter(Target=request.user).exclude(Actor=request.user)
    unread_subject_events = subject_events.filter(is_read=False)

    for notification in unread_subject_events:
        notification.is_read = True
        notification.save()

    paginator = Paginator(subject_events, 20)
    page = request.GET.get('page')
    if paginator.num_pages > 1:
        p = True
    else:
        p = False
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)

    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'user_accounts/activities.html', {
        'page': page,
        'p': p,
        'events': events
    })


@login_required
@ajax_required
def check_activities(request):
    subject_events = Notification.objects.filter(Target=request.user, is_read=False).exclude(Actor=request.user)
    return HttpResponse(len(subject_events))


@login_required
@ajax_required
def send_message_request(request, user_id):
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
    spammer = get_object_or_404(User, id=user_id)
    blocker = request.user

    if spammer in blocker.profile.contact_list.all():
        blocker.profile.contact_list.remove(spammer)
        spammer.profile.contact_list.remove(blocker)
        return redirect('user_profile', username=spammer)
    else:
        return redirect('/')


@throttle(zone='default')
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

    return render(request, 'user_accounts/view_all_message_requests.html', {
        'users': users,
        'page': page,
        'p': p,
        'p_obj': p_obj
    })


@throttle(zone='default')
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

    return render(request, 'user_accounts/view_all_contacts.html', {
        'users': users,
        'page': page,
        'p': p,
        'p_obj': p_obj
    })
