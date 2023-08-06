from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    
    # 토큰 발급 (access token)
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # 토큰 갱신 (refresh token)
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # 토큰 유효성 확인
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    
    path("api/users/", include("users.urls")),
    path("api/boards/", include("boards.urls")),
]
