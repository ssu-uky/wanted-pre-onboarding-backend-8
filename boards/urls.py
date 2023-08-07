from django.urls import path
from . import views

urlpatterns = [
    path("write/", views.BoardWriteView.as_view(), name="board-write"),
    path("list/", views.BoardListView.as_view(), name="board-list"),
    path("detail/<int:pk>/", views.BoardDetailView.as_view(), name="board-detail"),
]
