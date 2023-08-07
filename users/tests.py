# python manage.py test users.tests

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class UserAccountTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@test.com",
            "password": "test1234",
        }


    # 회원가입 테스트
    def test_signup(self):
        response = self.client.post(
            reverse("signup"),
            self.user_data,
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        
        # 잘못된 회원가입 시도
        response = self.client.post(
            reverse("signup"),
            {
                "email": "test",
                "password": "test",
            },
        )
        self.assertEqual(response.status_code, 400)


    # 로그인 테스트
    def test_login(self):
        
        self.test_signup() # 로그인 전 회원가입 먼저하기
        
        # 잘못된 로그인 시도
        response = self.client.post(
            reverse("login"),
            {
                "email": "test",
                "password": "test",
            },
        )
        self.assertEqual(response.status_code, 400)
        # print({"wrong login: "}, response.data) # error message == OK

        # 올바른 로그인 시도
        response = self.client.post(
            reverse("login"),
            self.user_data,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        # print({"login: "}, response.data)

        # # 로그인 후 토큰이 발급되었는지 확인(쿠키에 저장 됨)
        self.assertIn("refresh_token", response.cookies)
        
        # # 세션 ID가 발급되었는지 확인(쿠키에 저장 됨)
        self.assertIn("sessionid", response.cookies)

        # print({"save in cookie: "}, response.cookies) # Set-Cookie in csrftoken, refresh_token, sessionid == OK




    # 로그아웃 테스트
    def test_logout(self):
        self.test_login()  # 로그아웃 전 로그인 먼저하기
        
        # 로그인 후 refresh token, sessionid cookie 저장되어있는지 확인
        refresh_token = self.client.cookies["refresh_token"].value
        session_id = self.client.cookies["sessionid"].value
        
        
        # 로그아웃 시도
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        
        # 로그아웃 후 세션 id와 refresh token이 삭제되었는지 확인
        self.assertNotIn(refresh_token, self.client.cookies)
        self.assertNotIn(session_id , self.client.cookies)
        # print({"remove cookie: "}, self.client.cookies) # 삭제 완료
        
        # 유효하지 않은 토큰으로 로그인 시도
        self.client.cookies["refresh_token"] = "invalid_token"
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 400)
