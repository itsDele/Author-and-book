from celery import shared_task
from django.core.cache import cache
from book.models import Book

@shared_task
def remove_book_from_cache(book_id):
    """
    Remove a book from Redis cache when it's deleted
    """
    try:
        # Remove individual book cache
        cache.delete(f"book_{book_id}")
        
        # Remove from books list cache (will be regenerated on next request)
        cache.delete("all_books")
        
        print(f"✅ Removed book {book_id} from Redis cache")
        return f"Removed book {book_id} from cache"
        
    except Exception as e:
        print(f"❌ Error removing book from cache: {str(e)}")
        return f"Error: {str(e)}"