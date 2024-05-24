from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAuthorOrReadOnly, IsOwnerOrReadOnly
from .pagination import DefultPagination
from .models import Author, Category, Post, PostImage
from .serializers import (
    AuthorSerializer,
    CategorySerializer,
    PostImageSerializer,
    PostSerializer,
    CreatePostSerializer,
    UpdatePostSerializer,
)


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]

    @action(methods=["GET", "PUT"], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        author = Author.objects.get(user_id=request.user.id)
        if request.method == "GET":
            serializer = AuthorSerializer(author)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = AuthorSerializer(author, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        if Post.objects.filter(category_id=self.kwargs["pk"]).count() > 0:
            return Response(
                {"error": "can not delete this category"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class PostViewSet(ModelViewSet):
    http_method_names = ["get", "patch", "delete", "post", "head", "options"]
    queryset = Post.objects.all()
    pagination_class = DefultPagination
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreatePostSerializer
        if self.request.method == "PATCH":
            return UpdatePostSerializer
        return PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreatePostSerializer(
            data=request.data, context={"author_id": request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostImageViewSet(ModelViewSet):
    http_method_names = ["get", "delete", "post", "head", "options"]
    serializer_class = PostImageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return PostImage.objects.filter(post_id=self.kwargs["post_pk"])

    def get_serializer_context(self):
        return {"post_id": self.kwargs["post_pk"]}
