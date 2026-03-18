"""
Custom Middleware for Error Handling
"""

import logging
from django.shortcuts import render
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware:
    """
    Middleware to catch unhandled exceptions and provide user-friendly error pages
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            # Log the actual error for debugging
            logger.exception(f"Unhandled exception on {request.path}: {str(e)}")
            
            # Return user-friendly error response
            if request.path.startswith('/api/'):
                # For API endpoints, return JSON
                return JsonResponse({
                    'error': 'An unexpected error occurred. Please try again later.',
                    'status': 'error'
                }, status=500)
            else:
                # For regular pages, render error template
                return render(request, '500.html', status=500)
    
    def process_exception(self, request, exception):
        """
        Process exceptions that occur during request processing
        """
        # Log the exception
        logger.exception(f"Exception on {request.path}: {str(exception)}")
        
        # For API endpoints, return JSON
        if request.path.startswith('/api/'):
            return JsonResponse({
                'error': 'An unexpected error occurred. Please try again later.',
                'status': 'error'
            }, status=500)
        
        # For regular pages, let Django's handler500 handle it
        return None
