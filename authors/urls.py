from django.urls import path

from .views import RegisterView, LoginView, AuthorBooksView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "authors/<str:username>/books/", AuthorBooksView.as_view(), name="author-books"
    ),
]
