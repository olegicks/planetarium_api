from django.urls import path

from user.views import CreateUserView, LoginUserView, ManageUserView
from rest_framework_simplejwt.views import (
   TokenObtainPairView,
   TokenRefreshView,
)


urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

app_name = "user"
