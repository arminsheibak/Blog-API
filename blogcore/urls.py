from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()
router.register("authors", views.AuthorViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
