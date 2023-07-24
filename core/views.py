from django.shortcuts import render
from djoser.views import TokenCreateView
from .serializers import CustomTokenCreateSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
class CustomTokenCreateView(TokenObtainPairView):
    serializer_class = CustomTokenCreateSerializer
