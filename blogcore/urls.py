from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()
router.register("authors", views.AuthorViewSet)
router.register("categories", views.CategoryViewSet)
router.register("posts", views.PostViewSet)

posts_router = routers.NestedSimpleRouter(router, "posts", lookup="post")
posts_router.register("images", views.PostImageViewSet, basename="post-images")
posts_router.register("comments", views.CommentViewSet, basename="post-comments")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(posts_router.urls)),
]
