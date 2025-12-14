from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'author')

    def create(self, validated_data):
        # Set author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model"""
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'content',
            'created_at', 'updated_at', 'comments', 'comments_count', 'likes_count'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'author', 'comments')

    def get_comments_count(self, obj):
        """Get the number of comments for this post"""
        return obj.comments.count()

    def get_likes_count(self, obj):
        """Get the number of likes for this post"""
        return obj.likes.count()

    def create(self, validated_data):
        # Set author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """Simplified serializer for post lists"""
    author = serializers.StringRelatedField(read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'content',
            'created_at', 'updated_at', 'comments_count', 'likes_count'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'author')

    def get_comments_count(self, obj):
        """Get the number of comments for this post"""
        return obj.comments.count()

    def get_likes_count(self, obj):
        """Get the number of likes for this post"""
        return obj.likes.count()

