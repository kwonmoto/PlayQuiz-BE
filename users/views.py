from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import ( TokenObtainPairView,TokenRefreshView, )
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User

from django.shortcuts import redirect
from json import JSONDecodeError
from django.http import JsonResponse
import requests
import os
from rest_framework import status
from .models import *
from .utils import Util
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    SignupSerializer, 
    UserdateSerializer,
    CustomTokenObtainPairSerializer,
    LogoutSerializer
    )
class UserView(APIView):
    permission_classes = [AllowAny]
    def get_permissions(self):
        if self.request.method == "PUT" or self.request.method == "DELETE":
            return [IsAuthenticated(), ]
        return super(UserView, self).get_permissions()
    
    # 회원가입
    @swagger_auto_schema(
        request_body=SignupSerializer,
        operation_summary="회원가입",
        responses={201: "성공", 400: "인풋값 에러", 404: "찾을 수 없음", 500: "서버 에러"},
        )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
    # 회원정보 수정
    def put(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserdateSerializer(user, data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"회원정보 수정 완료"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 회원 비활성화
    @swagger_auto_schema(
        operation_summary="회원 비활성화",
        responses={200: "성공", 401: "인증 오류", 403: "접근 권한 에러", 500: "서버 에러"},
    )
    def delete(self, request):
        user = get_object_or_404(User, id=request.user.id)
        user.save()
        return Response({"message": "회원 비활성화"}, status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenViewBase):
    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        try:
            serializer.is_valid(raise_exception=True)
            # 로그인 로그 저장
            user_ip = Util.get_client_ip(request)
            country = Util.find_ip_country(user_ip)
            user = User.objects.get(userNameLoc=request.data["userNameLoc"])
            LoggedIn.objects.create(user=user, created_at=timezone.now(), updated_ip=user_ip, country=country)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=LogoutSerializer,
        operation_summary="로그아웃",
        responses={200: "성공", 400: "토큰 유효하지 않음", 401: "인증 에러", 500: "서버 에러"},
    )

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)