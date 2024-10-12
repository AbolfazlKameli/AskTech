from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from urllib.parse import urlencode


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
                'has_next': self.page.has_next(),
                'first': self.get_first_link(),
                'last': self.get_last_link()
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

    def get_first_link(self):
        if self.page.number == 1:
            return None
        return self.build_page_link(1)

    def get_last_link(self):
        if self.page.number == self.page.paginator.num_pages:
            return None
        return self.build_page_link(self.page.paginator.num_pages)

    def build_page_link(self, page_number):
        url = self.request.build_absolute_uri(self.request.path)
        query_params = self.request.GET.copy()
        query_params['page'] = page_number
        return f'{url}?{urlencode(query_params)}'
