from frontboard.models import Board, Comment, Subject
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView, UpdateAPIView)
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .pagination import (BoardLimitOffsetPagination, BoardPageNumberPagination,
                         SubjectLimitOffsetPagination,
                         SubjectPageNumberPagination)
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (BoardCreateUpdateSerializer, BoardListSerializer,
                          BoardRetrieveSerializer,
                          CommentCreateUpdateSerializer, CommentListSerializer,
                          SubjectCreateUpdateSerializer, SubjectListSerializer,
                          SubjectRetrieveSerializer)


class SubjectListAPIView(ListAPIView):
    serializer_class = SubjectListSerializer
    pagination_class = SubjectPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Subject.objects.all()
        user_query = self.request.GET.get('user', '')
        board_query = self.request.GET.get('board', '')
        if user_query or board_query:
            queryset_list = queryset_list.filter(
                author__username__icontains=user_query,
                board__title__icontains=board_query
            )
        return queryset_list


class SubjectRetrieveAPIView(RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectRetrieveSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class SubjectUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class SubjectDestroyAPIView(DestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectRetrieveSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


# untested view
class SubjectCreateAPIView(CreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BoardListAPIView(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer
    pagination_class = BoardPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']


class BoardRetrieveAPIView(RetrieveAPIView):
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


# untested view
class BoardCreateAPIView(CreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(admins.add(request.user))


class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.all()
        subject_slug = self.kwargs['slug']
        if subject_slug:
            queryset_list = queryset_list.filter(
                subject__slug__icontains=subject_slug
            )
        return queryset_list


# untested view
class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(commenter=self.request.user)
