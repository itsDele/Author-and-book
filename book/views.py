from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Book
from .serializers import Bookserializers

from rest_framework import viewsets


class BookCrud(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = Bookserializers
