from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

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
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=LoginSerializer,
        # responses={
        #     200: {
        #         "type": "object",
        #         "properties": {
        #             "user": UserSerializer,
        #             "tokens": {
        #                 "type": "object",
        #                 "properties": {
        #                     "access": {"type": "string"},
        #                     "refresh": {"type": "string"}
        #                 }
        #             }
        #         }
        #     },
        #     400: "Bad Request"
        # }
    )
    def post(self, request):
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
            }, "Login successful", 200)
        return responseWrapper(False,error=serializer.errors, message="Login failed", status_code=status.HTTP_400_BAD_REQUEST)
