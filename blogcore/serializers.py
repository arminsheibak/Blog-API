from rest_framework import serializers
from .models import Author, Category, Post, PostImage, Comment


class AuthorSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author
        fields = ["user_id", "bio", "birth_date", "phone"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "image"]

    def create(self, validated_data):
        post_id = self.context["post_id"]
        return PostImage.objects.create(post_id=post_id, **validated_data)


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "category",
            "author",
            "images",
            "content",
            "publication_date",
        ]


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "category", "content"]

    def save(self, **kwargs):
        author = Author.objects.get(user_id=self.context["author_id"])
        post = Post.objects.create(author=author, **self.validated_data)
        return self.instance


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "category", "content"]
