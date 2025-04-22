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
import logging
from django.core.mail import send_mail
from django.utils.html import escape
from django.core.mail import BadHeaderError
import random
from .models import PasswordResetOTP
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .serializers import OTPValidateSerializer, PasswordResetSerializer

User = get_user_model()
logger = logging.getLogger(__name__)
from rest_framework import status


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



def generate_otp():
    return str(random.randint(100000, 999999))

class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Check if a valid, unexpired OTP already exists
        existing_otp = PasswordResetOTP.objects.filter(user=user, is_used=False).order_by('-created_at').first()
        if existing_otp and not existing_otp.is_expired():
            return Response({
                "error": "An OTP has already been sent. Please wait 3 minutes before requesting again."
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        try:
            # Generate new OTP
            otp = f"{random.randint(100000, 999999)}"

            # Save new OTP
            PasswordResetOTP.objects.create(user=user, otp=otp)

            # Render email template
            userName = user.username.replace('.', ' ').title()
            html_content = render_to_string("emails/otp_email.html", {"userName": userName, "otp": otp})
            text_content = strip_tags(html_content)

            # Send email
            subject = "Your OTP for Password Reset"
            email_message = EmailMultiAlternatives(subject, text_content, None, [email])
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Failed to send OTP. {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ValidateOTPView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=OTPValidateSerializer)
    def post(self, request):
        serializer = OTPValidateSerializer(data=request.data)
        if serializer.is_valid():
            otp_obj = serializer.validated_data['otp_obj']
            otp_obj.is_used = False
            otp_obj.save()
            return Response({"error": "OTP is valid."}, status=status.HTTP_200_OK)

        # Extract first error message (can handle non_field_errors or custom keys)
        error_dict = serializer.errors
        first_key = next(iter(error_dict))
        error_message = error_dict[first_key][0] if isinstance(error_dict[first_key], list) else error_dict[first_key]
        
        return Response(
            {"error": error_message},
            status=status.HTTP_400_BAD_REQUEST
        )

class PasswordResetView(APIView):
    permission_classes = (permissions.AllowAny,)
    from .serializers import PasswordResetSerializer
    @swagger_auto_schema(request_body=PasswordResetSerializer)
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            otp_obj = serializer.validated_data['otp_obj']
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            # Mark OTP as used
            otp_obj.is_used = True
            otp_obj.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        error_dict = serializer.errors
        first_key = next(iter(error_dict))
        error_message = error_dict[first_key][0] if isinstance(error_dict[first_key], list) else error_dict[first_key]
        
        return Response(
            {"error": error_message},
            status=status.HTTP_400_BAD_REQUEST
        )


