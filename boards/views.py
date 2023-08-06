from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import BoardSerializer
from .models import WantedBoard


class BoardWriteView(APIView):
    """게시글 작성"""

    # 로그인 한 사용자만 가능
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({"message": "title, content, job_type, link(선택사항),file(선택사항)을 입력해주세요."}, status=status.HTTP_200_OK) 

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
            )

        board_data = {
            "writer": request.user.email,
            "title": request.data.get("title"),
            "content": request.data.get("content"),
            "job_type": request.data.get("job_type"),
        }

        serializer = BoardSerializer(data=board_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardListView(APIView):
    """게시글 목록 조회 with pagination"""

    def get(self, request):
        paginator = PageNumberPagination()
        queryset = WantedBoard.objects.all()
        context = paginator.paginate_queryset(queryset, request)
        serializer = BoardSerializer(context, many=True)
        return paginator.get_paginated_response(serializer.data)


class BoardDetailView(APIView):
    """게시글 pk로 조회, 수정, 삭제"""

    def get_object(self, pk):
        try:
            return WantedBoard.objects.get(pk=pk)
        except WantedBoard.DoesNotExist:
            return None

    # 게시글 조회
    def get(self, request, pk):
        board = self.get_object(pk)
        if board is None:
            return Response(
                {"message": "해당 게시글이 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = BoardSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 게시글 수정 == 작성자만 가능
    def put(self, request, pk):
        board = self.get_object(pk)

        if request.user.email != board.writer:
            return Response(
                {"message": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = BoardSerializer(
            board,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            update_board = serializer.save()
            return Response(
                BoardSerializer(update_board).data, status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제 == 작성자만 가능
    def delete(self, request, pk):
        board = self.get_object(pk)

        if request.user.email != board.writer:
            return Response(
                {"message": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

