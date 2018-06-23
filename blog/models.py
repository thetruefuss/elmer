from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from autoslug import AutoSlugField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=500)
    slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    photo = models.ImageField(upload_to='blog_posts/', blank=True, null=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-publish', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.slug])


class Comment(models.Model):

    post = models.ForeignKey(Post, related_name='comments')
    author = models.ForeignKey(User, related_name='post_comments')
    body = models.TextField(max_length=1000)

    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author, self.post)


class Image(models.Model):

    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='blog_photos/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.title


class Blog_Feedback(models.Model):

    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    message = models.TextField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.message
