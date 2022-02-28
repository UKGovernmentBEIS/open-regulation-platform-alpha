"""Custom paginator class."""

# Third Party
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Sub class Paginator class to allow page size to be set."""

    page_size_query_param = 'page_size'
