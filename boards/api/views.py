#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from boards.models import Board

from .pagination import BoardPageNumberPagination
from .permissions import IsAdminOrReadOnly
from .serializers import BoardSerializer


class BoardListCreateAPIView(ListCreateAPIView):
    """
    View that returns a list of boards & handles the creation of
    boards & returns data back.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BoardPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']


class BoardRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    View that retrieve, update or delete (if user is the admin of) the board.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class SubscribeBoardView(APIView):
    def get(self, request, format=None):
        """
        View that subscribe / unsubscribe a board and returns action status.
        """
        data = dict()
        user = request.user
        board_slug = request.GET.get('board_slug')
        board = Board.objects.get(slug=board_slug)
        user = request.user
        if board in user.subscribed_boards.all():
            board.subscribers.remove(user)
            data['is_subscribed'] = False
        else:
            board.subscribers.add(user)
            data['is_subscribed'] = True

        data['total_subscribers'] = board.subscribers.count()
        return Response(data)


class GetSubscribedBoards(APIView):
    def get(self, request, format=None):
        """Return a list of user subscribed boards."""
        boards = request.user.subscribed_boards.all()
        boards_list = [{'id': board.id, 'title': board.title} for board in boards]
        return Response(boards_list)


class TrendingBoardsList(APIView):
    def get(self, request, format=None):
        """Return a list of trending boards."""
        boards = Board.objects.all()
        trending_boards = sorted(boards, key=lambda instance: instance.recent_posts(), reverse=True)[:5]
        trending_boards_list = [{'title': board.title, 'slug': board.slug} for board in trending_boards]
        return Response(trending_boards_list)
