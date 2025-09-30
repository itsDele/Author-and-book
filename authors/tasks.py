# authors/tasks.py
from celery import shared_task
from .models import Author, Notifications
from book.models import Book


# authors/tasks.py
@shared_task
def notify_followers_new_book(book_data):
    """
    Send notifications to all followers when an author publishes a new book
    """
    try:
        print(f"🔍 Starting notify_followers_new_book with data: {book_data}")
        
        book_id = book_data.get('book_id')
        author_id = book_data.get('author_id')
        
        if not book_id or not author_id:
            print("❌ Missing book_id or author_id in task data")
            return "Missing required data"
        
        # Get the book and author
        book = Book.objects.get(id=book_id)
        author = Author.objects.get(id=author_id)
        
        print(f"🔍 Found book: {book.title}, author: {author.username}")
        
        # Get all followers (authors who have favorited this author)
        followers = author.favorited_by.all()
        follower_count = followers.count()
        
        print(f"🔍 Author {author.username} has {follower_count} followers")
        
        notification_count = 0
        for follower in followers:
            # Create notification for each follower
            message = f"{author.username} published a new book: '{book.title}'"
            print(f"🔍 Creating notification for {follower.username}: {message}")
            
            Notifications.objects.create(
                recipient=follower,
                message=message
            )
            notification_count += 1
        
        print(f"✅ Sent {notification_count} notifications for new book '{book.title}'")
        return f"Sent {notification_count} notifications"
        
    except Book.DoesNotExist:
        error_msg = f"❌ Book with id {book_id} not found"
        print(error_msg)
        return error_msg
    except Author.DoesNotExist:
        error_msg = f"❌ Author with id {author_id} not found"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"❌ Error sending book notifications: {str(e)}"
        print(error_msg)
        import traceback
        print(f"🔍 Full traceback: {traceback.format_exc()}")
        return f"Error: {str(e)}"

@shared_task
def send_bulk_notifications(notifications_data):
    """
    Send multiple notifications in bulk (optimized for large numbers)
    """
    notifications = []
    for data in notifications_data:
        notifications.append(
            Notifications(
                recipient_id=data['recipient_id'],
                message=data['message']
            )
        )  # Fixed: Added closing parenthesis and proper indentation
    
    # Bulk create for better performance
    Notifications.objects.bulk_create(notifications)
    print(f"✅ Created {len(notifications)} notifications in bulk")
    return f"Created {len(notifications)} notifications"