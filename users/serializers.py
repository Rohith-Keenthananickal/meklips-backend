from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

from utils.custom_response import responseWrapper

User = get_user_model()

class OTPValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        from .models import PasswordResetOTP

        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"otp_error": "Invalid email or OTP."})

        otp_obj = PasswordResetOTP.objects.filter(
            user=user, otp=attrs['otp'], is_used=False
        ).order_by('-created_at').first()

        if not otp_obj:
            raise serializers.ValidationError({"otp_error": "Invalid email or OTP."})

        if otp_obj.is_expired():
            raise serializers.ValidationError({"otp_error": "OTP has expired."})

        attrs['user'] = user
        attrs['otp_obj'] = otp_obj
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        from .models import PasswordResetOTP

        email = attrs.get('email')
        otp = attrs.get('otp')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "email": "No user found with this email address."
            })

        otp_obj = PasswordResetOTP.objects.filter(
            user=user, otp=otp, is_used=False
        ).order_by('-created_at').first()

        if not otp_obj:
            raise serializers.ValidationError({
                "otp": "Invalid OTP or it has already been used."
            })

        if otp_obj.is_expired():
            raise serializers.ValidationError({
                "otp": "OTP has expired."
            })

        attrs['user'] = user
        attrs['otp_obj'] = otp_obj
        return attrs

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'is_active')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        """
        Convert the user instance to a dictionary.
        """
        return super().to_representation(instance)

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'email': {'help_text': 'User email address'},
            'password': {'help_text': 'Password for the account (min 8 characters)'}
        }

    def create(self, validated_data):
        """
        Create a new user with the given data.
        Username is automatically set from email.
        """
        email = validated_data['email']
        # Use the part before @ as username, or if too long, use first 30 chars
        username = email.split('@')[0][:30]
        # Ensure username is unique by appending a number if needed
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            email=email,
            username=username,
            password=validated_data['password']
        )
        return responseWrapper(True, user, "User created successfully", 201)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            # First check if user exists
            user = User.objects.get(email=attrs['email'])
            
            # Then try to authenticate
            user = authenticate(username=user.username, password=attrs['password'])
            if not user or user is None:
                raise serializers.ValidationError('Invalid email or password')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
                
            return attrs
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')
        except Exception as e:
            raise serializers.ValidationError(f'Authentication error: {str(e)}') 