from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from throttle.decorators import throttle

from .forms import CommentForm
from .models import Blog_Feedback, Comment, Image, Post


@cache_page(60*1440)
@throttle(zone='default')
def post_list(request):
    all_posts = Post.published.all()
    recent_posts = Post.published.all()[:4]
    recent_comments = Comment.objects.order_by('-created')[:4]

    return render(request, 'blog/post/list.html', {
        'posts': all_posts,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        'home_active': True
    })


@throttle(zone='default')
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_body = request.POST.get('textarea')
        if comment_body is not None and len(comment_body) <= 1000:
            try:
                Comment.objects.create(post=post,
                                       author=request.user,
                                       body=comment_body)
                return redirect('post_detail', post.slug)
            except:  # noqa: E722
                comment_form = CommentForm()
        else:
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })


@throttle(zone='default')
def about(request):
    me = User.objects.get(username='eon')
    ali = User.objects.get(username='ali')
    return render(request, 'blog/about.html', {
        'me': me,
        'ali': ali,
        'about_active': True
    })


@throttle(zone='default')
def photos(request):
    images = Image.objects.all()
    return render(request, 'blog/photos.html', {
        'images': images,
        'photos_active': True
    })


@throttle(zone='default')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if len(name) <= 100 and len(email) <= 100 and '@' in email and len(message) <= 1000:
            Blog_Feedback.objects.create(
                name=name,
                email=email,
                message=message
            )
            return redirect('blog_contact')

    return render(request, 'blog/contact.html', {'contact_active': True})
