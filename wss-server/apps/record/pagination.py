from rest_framework.pagination import PageNumberPagination


class LogPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'size'
    max_page_size = 10
