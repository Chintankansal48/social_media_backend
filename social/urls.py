from django.urls import path
from .views import PostListCreateView, FeedView, FollowView, UnfollowView, UserActionView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView
from .views import APIRootView

urlpatterns = [
    path("", APIRootView.as_view(), name="api-root"),  # Add this line
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
    path("feed/", FeedView.as_view(), name="feed"),
    path("users/<str:username>/follow/", FollowView.as_view(), name="follow"),
    path("users/<str:username>/unfollow/", UnfollowView.as_view(), name="unfollow"),
    path("users/<str:username>/action/", UserActionView.as_view(), name="user-action"),
]