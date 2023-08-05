from django.urls import path
from . import views


urlpatterns = [
    # 회원가입
    path("signup/", views.SignUpView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("logout/", views.LogoutView.as_view()),
]
