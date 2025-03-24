from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers

def drf_serializer_to_openapi(serializer_class):
    """Convert a DRF serializer into an OpenAPI schema"""
    if not serializer_class:
        return openapi.Schema(type=openapi.TYPE_OBJECT)

    if isinstance(serializer_class, serializers.Serializer):
        fields = serializer_class.get_fields()
    elif issubclass(serializer_class, serializers.Serializer):
        fields = serializer_class().get_fields()
    else:
        return openapi.Schema(type=openapi.TYPE_OBJECT)

    properties = {
        field_name: drf_field_to_openapi(field)
        for field_name, field in fields.items()
    }

    return openapi.Schema(type=openapi.TYPE_OBJECT, properties=properties)

def drf_field_to_openapi(field):
    """Convert DRF Serializer fields to OpenAPI Schema"""
    if isinstance(field, serializers.CharField):
        return openapi.Schema(type=openapi.TYPE_STRING)
    elif isinstance(field, serializers.IntegerField):
        return openapi.Schema(type=openapi.TYPE_INTEGER)
    elif isinstance(field, serializers.BooleanField):
        return openapi.Schema(type=openapi.TYPE_BOOLEAN)
    elif isinstance(field, serializers.FloatField):
        return openapi.Schema(type=openapi.TYPE_NUMBER)
    elif isinstance(field, serializers.ListField):
        return openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=drf_field_to_openapi(field.child)
        )
    elif isinstance(field, serializers.DictField):
        return openapi.Schema(type=openapi.TYPE_OBJECT)
    elif isinstance(field, serializers.DateTimeField):
        return openapi.Schema(type=openapi.TYPE_STRING, format="date-time")
    elif isinstance(field, serializers.DateField):
        return openapi.Schema(type=openapi.TYPE_STRING, format="date")
    elif isinstance(field, serializers.Serializer):
        return drf_serializer_to_openapi(field)  # ✅ Handle Nested Serializers
    else:
        return openapi.Schema(type=openapi.TYPE_STRING)

def swagger_response(request_serializer=None, response_serializer=None, method=None):
    """Decorator to add Swagger documentation for request and response models"""
    
    def decorator(view_func):
        if method is None:
            raise ValueError("You must specify a method ('get', 'post', 'put', 'delete', etc.) in @swagger_response.")
        
        # ✅ Properly wrap response in common response model
        response_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Success status"),
                "data": drf_serializer_to_openapi(response_serializer) if response_serializer else openapi.Schema(type=openapi.TYPE_OBJECT),
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="Response message"),
                "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="Response status code"),
                "error": openapi.Schema(type=openapi.TYPE_OBJECT, description="Error details (if any)")
            }
        )

        return swagger_auto_schema(
            method=method,
            request_body=request_serializer,  
            responses={
                200: response_schema,
                400: openapi.Response("Bad Request"),
                404: openapi.Response("Not Found"),
            }
        )(view_func)

    return decorator
