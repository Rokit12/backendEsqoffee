from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .pagination import PostLimitOffsetPagination
from blog.models import Post, PostComment, PostCategory
from .permissions import IsOwnerOrReadOnly
from .mixins import MultipleFieldLookupMixin
from .serializers import (
    PostCategoryListSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
    CommentCreateUpdateSerializer,
)


class ListCategoryAPIView(ListAPIView):
    """
    get:
        Returns a list of all existing categories
    """
    queryset = PostCategory.objects.all()
    serializer_class = PostCategoryListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostLimitOffsetPagination


class ListCategoryDetailAPIView(APIView):
    """
       get:
           Returns the list of posts on a particular category
       """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        category = PostCategory.objects.get(slug=slug)
        posts = Post.objects.filter(category=category)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data, status=200)


class ListCommentAPIView(APIView):
    """
    get:
        Returns the list of comments on a particular post
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        comments = PostComment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)


class ListPostAPIView(ListAPIView):
    """
    get:
        Returns a list of all existing posts
    """

    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostLimitOffsetPagination


class DetailPostAPIView(APIView):
    """
    get:
        Returns the details of a post instance. Searches post using slug field.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        serializer = PostDetailSerializer(post, many=False)
        return Response(serializer.data, status=200)


class CreateCommentAPIView(APIView):
    """
    post:
        Create a comment instnace. Returns created comment data

        parameters: [slug, body]

    """

    serializer_class = CommentCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        serializer = CommentCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, parent=post)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)


class ListCommentAPIView(APIView):
    """
    get:
        Returns the list of comments on a particular post
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        comments = PostComment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)


class DetailCommentAPIView(MultipleFieldLookupMixin, RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the details of a comment instance. Searches comment using comment id and post slug in the url.

    put:
        Updates an existing comment. Returns updated comment data

        parameters: [parent, author, body]

    delete:
        Delete an existing comment

        parameters: [parent, author, body]
    """

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = PostComment.objects.all()
    lookup_fields = ["post", "id"]
    serializer_class = CommentCreateUpdateSerializer
