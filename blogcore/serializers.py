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
