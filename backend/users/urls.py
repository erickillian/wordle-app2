from django.urls import path
from users.views import *

urlpatterns = [
    path("login", UserLogin.as_view(), name="user_login"),
    path("logout", UserLogout.as_view(), name="user_logout"),
    path("remove_session", UserRemoveSession.as_view(), name="user_remove_session"),
    path("register", RegisterUserView.as_view(), name="user_registration"),
    path("users", UserListView.as_view(), name="user_list"),
    path("refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("self", UserSelfView.as_view(), name="user_self"),
    path("sessions", UserSessionListView.as_view(), name="user_sessions"),
]
