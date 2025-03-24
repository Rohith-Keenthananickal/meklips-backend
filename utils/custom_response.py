from rest_framework.response import Response

def responseWrapper(success, data=None, message=None, status_code=200, error=None):
    response_data = {
        "status": "success" if success else "error",
        "message": message,
        "statusCode": status_code
    }
    
    if success:
        response_data["data"] = data if data else []
    else:
        response_data["error"] = error if error else {}

    return Response(response_data, status=status_code)
