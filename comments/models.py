from django.contrib.auth.models import User
from django.db import models

from subjects.models import Subject


class Comment(models.Model):
    """
    Model that represents a comment.
    """
    subject = models.ForeignKey(Subject, related_name='comments', on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, related_name='posted_comments', on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    active = models.BooleanField(default=True)
    reply = models.ForeignKey(
        "Comment", related_name='comment_reply', null=True, blank=True, on_delete=models.SET_NULL
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        """Unicode representation for a comment model."""
        return self.body

    @staticmethod
    def get_comments(subject_slug=None):
        """Returns comments."""
        if subject_slug:
            comments = Comment.objects.filter(active=True,
                                              subject__slug__icontains=subject_slug)
        else:
            comments = Comment.objects.filter(active=True)
        return comments
