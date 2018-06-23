from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)


class SubjectLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 20


class SubjectPageNumberPagination(PageNumberPagination):
    page_size = 20


class BoardLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 20


class BoardPageNumberPagination(PageNumberPagination):
    page_size = 20
