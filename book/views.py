from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets

from .models import Book
from .serializers import Bookserializers

from authors.tasks import notify_followers_new_book




class BookCrud(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = Bookserializers
    
    def perform_create(self, serializer):
        instance = serializer.save()
        
        # Trigger notification task after book is created
        if instance.author:
            notify_followers_new_book.delay({
                'book_id': instance.id,
                'author_id': instance.author.id
            })
        
        return instance
