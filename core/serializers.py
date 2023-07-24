from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username','email', 'password', 'first_name', 'last_name']

class UserSerializer(BaseUserSerializer):
    is_staff = serializers.BooleanField(read_only = True)
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_wsadmin']

class SimpleUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'is_staff']

class CustomTokenCreateSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        ## This data variable will contain refresh and access tokens
        data = super().validate(attrs)
        ## You can add more User model's attributes like username,email etc. in the data dictionary like this.
        data['is_staff'] = self.user.is_staff
        return data