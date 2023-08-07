from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.tests import UserAccountTest


class BoardTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@test.com",
            "password": "test1234",
        }
        
        UserAccountTest.test_sign_up(self) # 회원가입

        refresh = RefreshToken.for_user(self)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}",
        )

        self.board_data = {
            "writer" : self.user_data["email"],
            "title": "test-title",
            "content": "test-content",
            "job_type": "test-job_type",
        }

    def test_board_write(self):
        response = self.client.post(
            reverse("board-write"),
            self.board_data,
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.data)
        print(response.data["message"])
