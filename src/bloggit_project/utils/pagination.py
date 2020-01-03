from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    #to make things easier
    def get_paginated_data(self, data, request):
        if self.page.has_next():
            next_page = self.page.next_page_number()
        else:
            next_page = None
        
        if self.page.has_previous():
            previous_page = self.page.previous_page_number()
        else:
            previous_page = None
            
        paginated_data = {
            'count': self.page.paginator.count,
            'next': next_page,
            'previous': previous_page,
            'results': data,
            'authenticated': request.user.is_authenticated
        }

        return paginated_data