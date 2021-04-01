#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from boards.models import Board
from reports.models import Report

from .serializers import ReportSerializer


class ReportListCreateAPIView(ListCreateAPIView):
    """
    View that returns reports list of a single board & handles the creation
    of reports & returns data back.
    """
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        """
        Only admins of the board can see the reports.
        """
        current_user = self.request.user
        boards_slug = self.request.GET.get('boards_slug', '')
        board = Board.objects.get(slug=boards_slug)
        if board:
            if current_user in board.admins.all():
                queryset_list = Report.get_reports(boards_slug)
                return queryset_list
        return []

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
