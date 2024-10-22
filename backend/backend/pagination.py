from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            {
                "results": data,
                "page": {
                    "page_size": self.page.paginator.per_page,
                    "current_page": self.page.number,
                    "total_pages": self.page.paginator.num_pages,
                    "count": self.page.paginator.count,
                    "has_next": self.page.has_next(),
                    "has_prev": self.page.has_previous(),
                },
            }
        )


class LargerResultsSetPagination(StandardResultsSetPagination):
    page_size = 20  # Set the pagination size to be larger
