from rest_framework import serializers
from .models import Post
from .models import UserAction
from .models import Follower

### Post Serializer
class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = ["id", "author", "content", "created_at"]


### Follower Serializer
class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ["follower", "following"]

### UserAction Serializer
class UserActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAction
        fields = ["user", "target_user", "action"]