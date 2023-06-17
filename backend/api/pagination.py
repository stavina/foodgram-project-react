from rest_framework.pagination import PageNumberPagination

from .parameters import PAGE_SIZE


class PageLimitPagination(PageNumberPagination):
    """Пагинатор."""

    page_size_query_param = "limit"
    page_size = PAGE_SIZE
