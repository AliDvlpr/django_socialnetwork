from core.serializers import UserSerializer
from rest_framework import serializers
from core.serializers import UserSerializer, SimpleUserSerializer
from .models import *
from core.models import User
import random

class WorkspacesUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspacesUsers
        fields = ['workspace', 'user']

class WorkspacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspaces
        fields = ["id", "name", "image", "description", "admin"]