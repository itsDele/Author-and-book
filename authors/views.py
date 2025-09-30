from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView,ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.core.cache import cache
from django.shortcuts import get_object_or_404

from .serializers import loginserializers, AuthorSerializer,NotificationSerializer
from .models import Author,Notifications

class RegisterView(APIView):
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Registerd successfully", "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serilizer = loginserializers(data=request.data, context={"request": request})
        if serilizer.is_valid():
            return Response(serilizer.validated_data, status=status.HTTP_200_OK)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.core.cache import cache

class AuthorBooksView(RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = "username"

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        cache_key = f"author_books:{username}"  # Create a unique key for this author
        
        # Try to get the data from the cache first
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
        
        # If not in cache, execute the original logic and database query
        response = super().retrieve(request, *args, **kwargs)
        
        # Store the response data in the cache for 15 minutes (900 seconds)
        cache.set(cache_key, response.data, timeout=900)
        
        return response
    
class FavoriteAuthorActionView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request,author_id):
        current_author = request.user
        target_author = get_object_or_404(Author,id=author_id)

        current_author.favorite_authors.add(target_author)
        return Response({
            "status": "success",
            "message": f"Added {target_author.username} to favorites",
            "favorited_author": {
                "id": target_author.id,
                "username": target_author.username,
                "first_name": target_author.first_name,
                "last_name": target_author.last_name
            }
        }, status=status.HTTP_201_CREATED)
    
class MyFavoritesListView(ListAPIView):
    """
    Get list of current user's favorite authors
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorSerializer

    def get_queryset(self):
        return self.request.user.favorite_authors.all()
    
class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return notifications for the logged-in author, newest first
        return Notifications.objects.filter(
            recipient=self.request.user
        ).order_by('-created_at')