from django.urls import path

from .views import RegisterView, LoginView, AuthorBooksView,FavoriteAuthorActionView,MyFavoritesListView,NotificationListView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "authors/<str:username>/books/", AuthorBooksView.as_view(), name="author-books"
    ),
    path("favorites/<int:author_id>/", FavoriteAuthorActionView.as_view(), name="favorite-action"),
    path("me/favorites/", MyFavoritesListView.as_view(), name="my-favorites"),
    path('notifications/', NotificationListView.as_view(), name='author-notifications'),
]
