from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets

from .models import Book
from .serializers import Bookserializers
from .tasks import remove_book_from_cache

from authors.tasks import notify_followers_new_book

class BookCrud(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = Bookserializers
    
    def get_queryset(self):
        """Override get_queryset to implement caching for list view"""
        if self.action == 'list':
            cache_key = "all_books"
            cached_books = cache.get(cache_key)
            if cached_books is not None:
                return cached_books
            
            books = super().get_queryset()
            cache.set(cache_key, books, timeout=60*300)  # Cache for 300 minutes (5 hours)
            return books
        return super().get_queryset()
    
    def retrieve(self, request, *args, **kwargs):
        """Cache individual book retrievals"""
        book_id = kwargs.get('pk')
        cache_key = f"book_{book_id}"
        
        # Try to get from cache first
        cached_book = cache.get(cache_key)
        if cached_book is not None:
            return Response(cached_book)
        
        # If not in cache, get from database and cache it
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60*300)  # Cache for 300 minutes (5 hours)
        return response  # Fixed: return the response object
    
    def perform_create(self, serializer):
        instance = serializer.save()
        
        # Clear the books list cache when new book is added
        cache.delete("all_books")
        
        # Trigger notification task after book is created
        if instance.author:
            notify_followers_new_book.delay({
                'book_id': instance.id,
                'author_id': instance.author.id
            })
        
        return instance
    
    def perform_destroy(self, instance):
        book_id = instance.id
        
        # Call parent to actually delete the book
        super().perform_destroy(instance)
        
        # Trigger Celery task to remove from cache
        remove_book_from_cache.delay(book_id)