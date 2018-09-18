from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from subjects.models import Subject

from .pagination import SubjectPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import SubjectSerializer


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
                board__slug__icontains=board_query
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


class ActiveThreadsList(APIView):

    def get(self, request, format=None):
        """Return a list of active threads."""
        current_user = request.user
        active_threads = current_user.posted_subjects.all()[:5]
        active_threads_list = [
            {'title': thread.title,
             'slug': thread.slug,
             'board_slug': thread.board.slug} for thread in active_threads
        ]
        return Response(active_threads_list)
