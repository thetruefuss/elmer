#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)


class BoardLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 20


class BoardPageNumberPagination(PageNumberPagination):
    page_size = 20
