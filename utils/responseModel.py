from typing import Any, Optional
from django.http import JsonResponse
from http import HTTPStatus

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