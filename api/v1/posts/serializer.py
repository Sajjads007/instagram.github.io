from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Post, UserAccount, Comments

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id','comment','user_name')


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id','name','profile_picture','bio', 'user')


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    like = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id','image','caption','like','like_count','comments','user_name')

    def get_like(self, instance):
        return instance.like.name


class MyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','image', 'caption')


class DeletePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','is_deleted')


