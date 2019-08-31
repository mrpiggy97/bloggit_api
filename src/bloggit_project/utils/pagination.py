from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    #to make things easier
    def get_paginated_data(self, data):
        paginated_data = {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        }

        return paginated_data