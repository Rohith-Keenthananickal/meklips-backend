from typing import Any, Optional, Callable, Type
from django.http import JsonResponse, HttpResponse
from http import HTTPStatus
from functools import wraps
from django.views import View

def create_response(
    status: str,
    code: int,
    data: Any = None,
    error: Optional[str] = None
) -> JsonResponse:
    """
    Create a standardized JSON response.
    
    Args:
        status (str): Response status (e.g., 'success', 'error')
        code (int): HTTP status code
        data (Any, optional): Response data
        error (str, optional): Error message if any
    
    Returns:
        JsonResponse: Standardized JSON response
    """
    response_data = {
        'status': status,
        'code': code,
    }
    
    if data is not None:
        response_data['data'] = data
        
    if error is not None:
        response_data['error'] = error
        
    return JsonResponse(response_data, status=code)

def success_response(data: Any = None, code: int = HTTPStatus.OK) -> JsonResponse:
    """
    Create a success response.
    
    Args:
        data (Any, optional): Response data
        code (int, optional): HTTP status code (default: 200)
    
    Returns:
        JsonResponse: Success response
    """
    return create_response('success', code, data=data)

def error_response(error: str, code: int = HTTPStatus.BAD_REQUEST) -> JsonResponse:
    """
    Create an error response.
    
    Args:
        error (str): Error message
        code (int, optional): HTTP status code (default: 400)
    
    Returns:
        JsonResponse: Error response
    """
    return create_response('error', code, error=error)

def api_response(view_func: Callable) -> Callable:
    """
    Decorator to automatically wrap view responses in standard format.
    
    Usage:
        @api_response
        def your_view(request):
            # Your view logic here
            return data  # or raise Exception for errors
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            result = view_func(*args, **kwargs)
            
            # If result is already a JsonResponse, return it as is
            if isinstance(result, JsonResponse):
                return result
                
            # If result is a HttpResponse with non-200 status, treat as error
            if isinstance(result, HttpResponse) and result.status_code != 200:
                return error_response(
                    error=str(result.content.decode()),
                    code=result.status_code
                )
                
            # For successful responses
            return success_response(data=result)
            
        except Exception as e:
            # Handle exceptions and return error response
            return error_response(
                error=str(e),
                code=getattr(e, 'status_code', HTTPStatus.INTERNAL_SERVER_ERROR)
            )
    
    return wrapper

def api_view(cls: Type[View]) -> Type[View]:
    """
    Class decorator to automatically wrap all HTTP method responses in standard format.
    
    Usage:
        @api_view
        class YourView(View):
            def get(self, request):
                return {'data': 'value'}
                
            def post(self, request):
                return {'data': 'value'}
    """
    # Get all HTTP methods from the class
    http_methods = ['get', 'post', 'put', 'patch', 'delete']
    
    # Wrap each HTTP method with the api_response decorator
    for method in http_methods:
        if hasattr(cls, method):
            setattr(cls, method, api_response(getattr(cls, method)))
    
    return cls

def api_method(method_func: Callable) -> Callable:
    """
    Method decorator to wrap specific class-based view methods in standard format.
    
    Usage:
        class YourView(View):
            @api_method
            def get(self, request):
                return {'data': 'value'}
    """
    return api_response(method_func) 