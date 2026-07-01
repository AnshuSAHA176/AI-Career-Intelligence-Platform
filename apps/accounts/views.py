from django.shortcuts import render
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import RegisterSerializer,LoginSerializer,UserProfileSerializer,ProfileSerializer
from .models import User

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        refresh=RefreshToken.for_user(user)
        access=refresh.access_token
        return Response({
                    "access": str(access),
                    "refresh": str(refresh)
                },status=status.HTTP_200_OK)
class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=self.request.user
        serializer=UserProfileSerializer(user)
        return Response(serializer.data)
    def put(self,request):
        profile=request.user.profile
        serializer=ProfileSerializer(profile,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
