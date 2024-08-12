from typing import Any
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.db import connection

class SQLPrintingMiddleware(object):

    """ Middleware to print Number of Database Queries and time taken by this API Call"""

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        if not getattr(settings, "DEBUG", False):
            raise MiddlewareNotUsed
        
    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request,response)
    
    def process_response(self, request, response):
        if len(connection.queries)==0:
            return response
        total_time = 0.0
        for query in connection.queries:
            total_time += float(query["time"])

        # green text
        print(f"  \033[1;32m[TOTAL TIME:{total_time} seconds ({len(connection.queries)} queries)]\033[0m")
        # # yellow text
        # print(f"  \033[1;33m[TOTAL TIME:{total_time} seconds ({len(connection.queries)} queries)]\033[0m")
        # black text with backgound color white
        # print(f"  \033[1;30;47m[TOTAL TIME:{total_time} seconds ({len(connection.queries)} queries)]\033[0m")

        
        return response