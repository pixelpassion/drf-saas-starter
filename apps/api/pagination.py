from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """ This is a Pagination handler for django-rest-framework"""

    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200
