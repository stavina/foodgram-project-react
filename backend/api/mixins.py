from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import PageNumberPagination
from api.permissions import (AuthenticatedUsersOrReadOnly,
                               ListOrAllForEditAdminOnly
                               )


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class ReviewGenreModelMixin(ListCreateDestroyViewSet):
    permission_classes = [
        AuthenticatedUsersOrReadOnly,
        ListOrAllForEditAdminOnly
    ]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
