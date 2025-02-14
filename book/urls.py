from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import BookCrud


router = DefaultRouter()
router.register("books", BookCrud)

urlpatterns = [path("", include(router.urls))]
