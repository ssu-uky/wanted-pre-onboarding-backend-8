# python manage.py test boards.tests

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import WantedBoard


class BoardTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = {
            "email": "test@test.com",
            "password": "test1234",
        }

        self.board_data = {
            "writer": self.user["email"],
            "title": "test title",
            "content": "test content",
            "job_type": "PM",
        }

        # 게시글 생성 (하단 pk 조회용)
        self.board = WantedBoard.objects.create(**self.board_data)

    def new_user(self):
        response = self.client.post(
            "/api/users/signup/",
            self.user,
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        # print({"new user: "}, response.data)
        return response

    def login_user(self):
        response = self.client.post(
            "/api/users/login/",
            self.user,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        return response

    def authenticate(self):
        self.new_user()
        response = self.login_user()
        refresh_token = response.data["token"]["refresh_token"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + refresh_token)


    # 다른 유저 생성 (수정/삭제 테스트용)
    def authenticate_as_another_user(self):
        another_user = {
            "email": "wanted@wanted.com",
            "password": "wanted1234",
        }

        response = self.client.post(
            "/api/users/signup/",
            another_user,
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            "/api/users/login/",
            another_user,
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        refresh_token = response.data["token"]["refresh_token"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + refresh_token)


    # 게시글 작성 테스트 / POST
    def test_board_write(self):
        self.authenticate()

        response = self.client.post(
            reverse("board-write"),
            self.board_data,
            format="json",
        )
        self.assertEqual(response.status_code, 201)


    # 게시글 목록 조회 테스트 / [ALLOWANY] / LIST / GET
    def test_board_list(self):
        response = self.client.get(
            reverse("board-list"),
            format="json",
        )
        self.assertEqual(response.status_code, 200)


    # 게시글 PK로 상세 조회 테스트 / PK / GET
    def test_get_board_detail(self):
        # self.authenticate()
        board_pk = self.board.pk

        response = self.client.get(f"/api/boards/detail/{board_pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.board_data["title"]) # 조회한 pk의 title이 일치하는지 확인


    # 게시글 PK로 상세 조회 테스트 / PUT
    def test_update_board_detail(self):
        self.authenticate()
        board_pk = self.board.pk

        update_data = {
            "title": "update title",
            "content": "update content",
            "job_type": "FRONTEND",
        }
        
        response = self.client.put(
            f"/api/boards/detail/{board_pk}/",
            update_data,
            format="json",
        )
        # print({"update board detail: "}, response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], update_data["title"]) # 수정된 title 확인
    
    
    # 게시글 PK로 상세 조회 테스트 / DELETE
    def test_delete_board_detail(self):
        self.authenticate()
        board_pk = self.board.pk

        # 게시글 삭제
        response = self.client.delete(f"/api/boards/detail/{board_pk}/")
        self.assertEqual(response.status_code, 204)
        
        # 게시글이 실제로 삭제되었는지 확인
        response = self.client.get(f"/api/boards/detail/{board_pk}/")
        self.assertEqual(response.status_code, 404)



    # 게시글 작성자가 아닌 다른 유저가 게시글 수정 시도 테스트
    def test_update_board_detail_not_writer(self):
        self.authenticate_as_another_user()
        
        board_pk = self.board.pk
        update_data = {
            "title": "Hi title",
            "job_type": "BACKEND",
        }
        
        response = self.client.put(
            f"/api/boards/detail/{board_pk}/",
            update_data,
            format="json",
        )
        self.assertEqual(response.status_code, 403)
        # self.assertEqual(response.data,{"detail", "작성자만 수정할 수 있습니다."})
    
    
    # 게시글 작성자가 아닌 다른 유저가 게시글 삭제 시도 테스트
    def test_delete_board_detail_not_writer(self):
        self.authenticate_as_another_user()
        
        board_pk = self.board.pk
        response = self.client.delete(f"/api/boards/detail/{board_pk}/")
        self.assertEqual(response.status_code, 403)