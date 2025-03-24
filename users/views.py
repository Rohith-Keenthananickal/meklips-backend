from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from utils.custom_response import responseWrapper
from utils.decorators import swagger_response
from .serializers import UserSerializer, SignupSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()


class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses={201: UserSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        try:
            # Check if user with email already exists
            email = request.data.get('email')
            if User.objects.filter(email=email).exists():
                return responseWrapper(False, error="A user with this email already exists", message="Signup failed", status_code=status.HTTP_400_BAD_REQUEST)

            serializer = SignupSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return responseWrapper(True, UserSerializer(user).data, "User created successfully", status.HTTP_201_CREATED)
            return responseWrapper(False, error=serializer.errors, message="Signup failed", status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return responseWrapper(False, error=str(e), message="Signup failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=LoginSerializer,
    )
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = User.objects.get(email=serializer.validated_data['email'])
                refresh = RefreshToken.for_user(user)
                
                return responseWrapper(True, {
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, "Login successful", status_code=200)
            return responseWrapper(False, error=serializer.errors, message="Login failed", status_code=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            # Extract the actual error message from the ValidationError
            error_message = str(e.detail[0]) if isinstance(e.detail, list) else str(e.detail)
            return responseWrapper(False, error=error_message, message="Login failed", status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return responseWrapper(False, error=str(e), message="Login failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
