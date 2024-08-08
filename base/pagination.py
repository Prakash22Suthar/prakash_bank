from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            {
                "current_page": self.page.number,
                "num_pages": self.page.paginator.num_pages,
                "start_idex":self.page.start_index(),
                "end_index":self.page.end_index(),
                "count": self.page.paginator.count,
                "next":self.get_next_link(),
                "previous":self.get_previous_link(),
                "result":data,
            }
        )