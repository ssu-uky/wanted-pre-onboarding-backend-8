from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers


# 이메일 회원가입
class SignUpView(APIView):
    def get(self, request):
        return Response({"message": "이메일, 비밀번호를 입력해주세요."})

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        serializer = serializers.SignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if not (email and password):
                return Response({"message": "모든 값을 입력해주세요."},status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            user.save()

            new_user = Response(
                {
                    "message": "회원가입이 완료되었습니다. 로그인을 해주세요.",
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
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # 유저가 있다면 로그인 + 유지
            login(request, user)

            # jwt token 생성
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response(
                {
                    "message": "로그인 성공!",
                    "email": user.email,
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            # refresh token을 cookie에 저장
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            return response

        else:
            return Response(
                {"message": "이메일과 비밀번호를 확인해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# 로그아웃
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                # refresh token을 blacklist에 추가하여 만료시키기
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
                response = Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)
                response.delete_cookie("refresh_token")
                
                # session 에 저장된 id값도 지우기
                logout(request)
                
                return response
            except TokenError:
                return Response({"message": "토큰이 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "로그아웃 실패"}, status=status.HTTP_400_BAD_REQUEST)