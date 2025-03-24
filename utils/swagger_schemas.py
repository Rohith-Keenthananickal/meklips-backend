from drf_yasg import openapi

common_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(type=openapi.TYPE_STRING, description="success/error"),
        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Response message"),
        "data": openapi.Schema(type=openapi.TYPE_OBJECT, description="Response data (varies by API)"),
    },
)
