from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Post, Follower, UserAction
from .serializers import PostSerializer, FollowerSerializer, UserActionSerializer
from rest_framework.permissions import AllowAny

# Post List and Create View
class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Follow a User
class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target_user = get_object_or_404(User, username=username)
        if target_user == request.user:
            return Response({"error": "You cannot follow yourself."}, status=400)

        Follower.objects.get_or_create(follower=request.user, following=target_user)
        return Response({"message": f"You are now following {username}."})

# Unfollow a User
class UnfollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target_user = get_object_or_404(User, username=username)
        follow_relation = Follower.objects.filter(follower=request.user, following=target_user)
        if follow_relation.exists():
            follow_relation.delete()
            return Response({"message": f"You have unfollowed {username}."})
        return Response({"error": "You are not following this user."}, status=400)

# User Action (Hide/Block)
class UserActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        action = request.data.get("action")
        target_user = get_object_or_404(User, username=username)

        if target_user == request.user:
            return Response({"error": "You cannot perform this action on yourself."}, status=400)

        if action not in ["HIDE", "BLOCK"]:
            return Response({"error": "Invalid action."}, status=400)

        UserAction.objects.get_or_create(user=request.user, target_user=target_user, action=action)
        return Response({"message": f"User {username} has been {action.lower()}ed."})

    def delete(self, request, username):
        action = request.data.get("action")
        target_user = get_object_or_404(User, username=username)
        user_action = UserAction.objects.filter(user=request.user, target_user=target_user, action=action)

        if user_action.exists():
            user_action.delete()
            return Response({"message": f"Action {action} on user {username} has been removed."})
        return Response({"error": "Action not found."}, status=400)

# Feed View
class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hidden_users = UserAction.objects.filter(user=request.user, action="HIDE").values_list("target_user", flat=True)
        blocked_users = UserAction.objects.filter(user=request.user, action="BLOCK").values_list("target_user", flat=True)

        posts = Post.objects.filter(
            author__in=request.user.following.values_list("following", flat=True)
        ).exclude(
            author__in=hidden_users
        ).exclude(
            author__in=blocked_users
        ).order_by("-created_at")

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# User Registration
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users to access this endpoint

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User registered successfully."}, status=201)


class APIRootView(APIView):
    def get(self, request):
        return Response({
            "auth_register": "/api/auth/register/",
            "auth_login": "/api/auth/login/",
            "auth_refresh": "/api/auth/refresh/",
            "posts": "/api/posts/",
            "feed": "/api/feed/",
            "follow_user": "/api/users/<username>/follow/",
            "unfollow_user": "/api/users/<username>/unfollow/",
            "user_action": "/api/users/<username>/action/"
        })