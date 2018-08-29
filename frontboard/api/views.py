from frontboard.models import Board, Comment, Subject, Report
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (DestroyAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .pagination import BoardPageNumberPagination, SubjectPageNumberPagination
from .permissions import (IsAdminOrReadOnly, IsAuthorOrReadOnly,
                          IsCommenterOrReadOnly)
from .serializers import BoardSerializer, CommentSerializer, SubjectSerializer, ReportSerializer


class SubjectListCreateAPIView(ListCreateAPIView):
    """
    View that returns subjects list based on rank_score, specific user or
    board submissions etc & handles the creation of subjects & returns data back.
    """
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = SubjectPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Subject.get_subjects()

        user_query = self.request.GET.get('user', '')
        board_query = self.request.GET.get('board', '')
        trending_subjects = self.request.GET.get('trending', '')

        if user_query:
            queryset_list = queryset_list.filter(
                author__username__icontains=user_query,
            )
        if board_query:
            queryset_list = queryset_list.filter(
                board__title__icontains=board_query
            )
        if trending_subjects == "True":
            queryset_list = queryset_list.order_by('-rank_score')

        return queryset_list

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SubjectRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    View that retrieve, update or delete (if user is the author of) the subject.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class BoardListCreateAPIView(ListCreateAPIView):
    """
    View that returns a list of boards & handles the creation of boards & returns data back.
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


class StarSubjectView(APIView):

    def get(self, request, format=None):
        """
        View that star / unstar a subject and returns action status & total points.
        """
        data = dict()
        user = request.user
        subject_slug = request.GET.get('subject_slug')
        subject = Subject.objects.get(slug=subject_slug)
        user = request.user
        if subject in user.liked_subjects.all():
            subject.points.remove(user)
            data['is_starred'] = False
        else:
            subject.points.add(user)
            data['is_starred'] = True

        data['total_points'] = subject.points.count()
        return Response(data)


class GetSubscribedBoards(APIView):

    def get(self, request, format=None):
        """
        Return a list of user subscribed boards.
        """
        boards = request.user.subscribed_boards.all()
        boards_list = [{'id': board.id, 'title': board.title} for board in boards]
        return Response(boards_list)


class TrendingBoardsList(APIView):

    def get(self, request, format=None):
        """
        Return a list of trending boards.
        """
        boards = Board.objects.all()
        trending_boards = sorted(boards, key=lambda instance: instance.recent_posts(), reverse=True)[:5]
        trending_boards_list = [{'title': board.title, 'slug': board.slug} for board in trending_boards]
        return Response(trending_boards_list)


class ActiveThreadsList(APIView):

    def get(self, request, format=None):
        """
        Return a list of active threads.
        """
        current_user = request.user
        active_threads = current_user.posted_subjects.all()[:5]
        active_threads_list = [
            {'title': thread.title,
             'slug': thread.slug,
             'board_slug': thread.board.slug} for thread in active_threads
        ]
        return Response(active_threads_list)
