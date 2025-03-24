from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from utils.decorators import swagger_response
from .serializers import UserSerializer, SignupSerializer
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
