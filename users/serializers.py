from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'is_active')
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
        fields = ('email', 'username', 'password')
        extra_kwargs = {
            'email': {'help_text': 'User email address'},
            'username': {'help_text': 'Username for the account'},
            'password': {'help_text': 'Password for the account (min 8 characters)'}
        }

    def create(self, validated_data):
        """
        Create a new user with the given data.
        """
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user 