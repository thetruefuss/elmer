#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.generics import DestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from comments.models import Comment

from .permissions import IsCommenterOrReadOnly
from .serializers import CommentSerializer


class CommentListCreateAPIView(ListCreateAPIView):
    """
    View that returns comments list of a single subject & handles the creation
    of comments & returns data back.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        subject_slug = self.request.GET.get('subject_slug', '')
        queryset_list = Comment.get_comments(subject_slug)
        return queryset_list

    def perform_create(self, serializer):
        serializer.save(commenter=self.request.user)


class CommentDestroyAPIView(DestroyAPIView):
    """
    View that delete (if user is the commenter of) the comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommenterOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
