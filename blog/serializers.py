import os

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Post, PostComment, PostCategory

User = get_user_model()


class PostListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
            "image",
            "comments",
        ]

    def get_comments(self, obj):
        qs = PostComment.objects.filter(post=obj).count()
        return qs


class PostDetailSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "slug",
            "title",
            "body",
            "author",
            "image",
            "created_at",
            "updated_at",
            "comments",
        ]

    def get_slug(self, obj):
        return obj.slug

    def get_comments(self, obj):
        qs = PostComment.objects.filter(post=obj)
        try:
            serializer = CommentSerializer(qs, many=True)
        except Exception as e:
            print(e)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = [
            "id",
            "post",
            "author",
            "body",
            "created_at",
            "updated_at",
        ]


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = [
            "body",
        ]
