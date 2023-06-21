from rest_framework.pagination import PageNumberPagination

from django.conf import PAGE_SIZE


class PageLimitPagination(PageNumberPagination):
    """Пагинатор."""
    page_size_query_param = 'limit'
    page_size = PAGE_SIZE
