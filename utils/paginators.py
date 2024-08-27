from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class NeatPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 20
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        current_page = self.page.number
        paginator = self.page.paginator

        return Response({
            'pagination': {
                'current_page': current_page,
                'items_count': paginator.count,
                'pages_count': paginator.num_pages,
                'previous_page': self.get_previous_link(),
                'next_page': self.get_next_link(),
                'has_previous': self.page.has_previous(),
                'has_next': self.page.has_next()
            },
            'data': data
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'required': ['count', 'results'],
            'properties': {
                'current_page': {
                    'type': 'integer',
                    'example': 3,
                },
                'items_count': {
                    'type': 'integer',
                    'nullable': True,
                    'example': 32,
                },
                'pages_count': {
                    'type': 'integer',
                    'example': 4,
                },
                'previous_page': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'http://api.example.org/accounts/?{page_query_param}=2'.format(
                        page_query_param=self.page_query_param)
                },
                'next_page': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'http://api.example.org/accounts/?{page_query_param}=4'.format(
                        page_query_param=self.page_query_param)
                },
                'has_previous': {
                    'type': 'boolean',
                    'example': True,
                },
                'has_next': {
                    'type': 'boolean',
                    'example': True,
                },
                'data': schema,
            },
        }
