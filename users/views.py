from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from . import serializers


# 이메일 회원가입
class SignUpView(APIView):
    def get(self, request):
        return Response({"message": "이름, 이메일, 비밀번호를 입력해주세요."})

    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        serializer = serializers.SignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if not (name and email and password):
                return Response(
                    {"message": "모든 값을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST
                )

            user = serializer.save()
            user.save()

            new_user = Response(
                {
                    "message": "회원가입이 완료되었습니다. 로그인을 해주세요.",
                    "name": user.name,
                    "email": user.email,
                    "password": user.password,
                },
                status=status.HTTP_201_CREATED,
            )
            return new_user


# 로그인
class LoginView(APIView):
    def get(self, request):
        return Response({"message": "이메일, 비밀번호를 입력해주세요."})

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not (email and password):
            return Response(
                {"message": "이메일과 비밀번호를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST
            )

        # db에 저장되어 있는 데이터로 유저 데이터 인증
        user = authenticate(email=email, password=password)

        if user is None:
            return Response(
                {"message": "로그인 실패! 이메일과 비밀번호를 확인해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 로그인 시 토큰만 발행하면 로그인 유지가 되지 않아서 이렇게 로그인을 유지시킴
        login(request, user)

        # simple jwt token 생성
        token = TokenObtainPairSerializer().get_token(user) # refresh token 생성
        refresh_token = str(token) # refresh token 문자열로 변환
        access_token = str(token.access_token) # access token 문자열로 변환

        response = Response(
            {
                "message": "로그인 성공!",
                "name": user.name,
                "email": user.email,
                "token": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            },
            status=status.HTTP_200_OK,
        )
        
        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)
        return response


# 로그아웃
class LogoutView(APIView):
    def post(self, request):
        access_token = request.data.get("access_token")

        if access_token:
            try:
                # 유효한 access token인지 확인하고 블랙리스트에 추가
                token = RefreshToken(access_token)
                OutstandingToken.objects.create(token=token)
            except OutstandingToken.DoesNotExist:
                pass

        # 세션 저장 되어 있는 토큰 초기화
        # request.session.flush()

        logout(request)
        response = Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
        return response
