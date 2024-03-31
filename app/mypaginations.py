from rest_framework.pagination import LimitOffsetPagination

class MyPagination(LimitOffsetPagination):
    default_limit = 5
    page_size = 5
    max_limit = 10
    # limit_query_param = 'limit'
    # offset_query_param = 'offset'
    # limit_query_param = 'mylimit'
    # offset_query_param = 'myoffset'
    # def get_paginated_response(self, data):
    #     return {
    #         'next': self.get_next_link(),
    #         'previous': self.get_previous_link(),
    #         'count': self.count,
    #         'results': data
    #     }
    