from django.db import models
from django.contrib.auth import get_user_model
from .validator import validate_file_size


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Author(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, primary_key=True
    )
    profile_picture = models.ImageField(
        upload_to="blogcore/profile_picture", validators=[validate_file_size]
    )
    bio = models.CharField(max_length=520)
    birth_date = models.DateField()
    phone = models.CharField(max_length=14)


class Post(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        upload_to="blogcore/post_images", validators=[validate_file_size]
    )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    email = models.EmailField()
    body = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
