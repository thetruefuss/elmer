from frontboard.models import Board, Comment, Subject
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView, UpdateAPIView,
                                     ListCreateAPIView)
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from .pagination import (BoardLimitOffsetPagination, BoardPageNumberPagination,
                         SubjectLimitOffsetPagination,
                         SubjectPageNumberPagination)
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (BoardCreateUpdateSerializer, BoardListSerializer,
                          BoardRetrieveSerializer, CommentSerializer,
                          SubjectSerializer)


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
        trending_boards = sorted(boards, key=lambda instance:instance.recent_posts(), reverse=True)[:5]
        trending_boards_list = [{'title': board.title, 'slug': board.slug} for board in trending_boards]
        return Response(trending_boards_list)


class ActiveThreadsList(APIView):

    def get(self, request, format=None):
        """
        Return a list of active threads.
        """
        current_user = request.user
        active_threads = current_user.posted_subjects.all()[:5]
        active_threads_list = [{'title': thread.title, 'slug': thread.slug, 'board_slug': thread.board.slug} for thread in active_threads]
        return Response(active_threads_list)


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


class SubjectRetrieveAPIView(RetrieveAPIView):
    """
    View that returns data of single subject.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class SubjectUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class SubjectDestroyAPIView(DestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class BoardListAPIView(ListAPIView):
    """
    View that returns a list of boards.
    """
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer
    pagination_class = BoardPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']


class BoardRetrieveAPIView(RetrieveAPIView):
    """
    View that returns board details.
    """
    queryset = Board.objects.all()
    serializer_class = BoardRetrieveSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


# untested view
class BoardUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def perform_update(self, serializer):
        serializer.save(admins.add(request.user))


class BoardDestroyAPIView(DestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardRetrieveSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class BoardCreateAPIView(CreateAPIView):
    """
    View that handles the creation of boards & returns data back.
    """
    queryset = Board.objects.all()
    serializer_class = BoardCreateUpdateSerializer
    permission_classes = [IsAuthenticated]


class CommentListAPIView(ListAPIView):
    """
    View that lists the comments on single subject.
    """
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.all()
        subject_slug = self.kwargs['slug']
        if subject_slug:
            queryset_list = queryset_list.filter(
                subject__slug__icontains=subject_slug
            )
        return queryset_list


class CommentCreateAPIView(CreateAPIView):
    """
    View that handles the creation of comments & return data back.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(commenter=self.request.user)
