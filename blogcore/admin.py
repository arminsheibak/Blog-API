from django.contrib import admin
from .models import Author, Post, PostImage, Category

admin.site.site_header = "Blog Admin"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email"]
    list_select_related = ["user"]
    list_per_page = 10


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "publication_date"]
    list_select_related = ["author", "category"]
    list_per_page = 10
    search_fields = ["title__istartswith"]


admin.site.register(Category)
admin.site.register(PostImage)
