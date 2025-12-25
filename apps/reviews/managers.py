from django.db import models

class ReviewsManager(models.Manager):
    
    def by_book(self, book_id):
        return self.filter(book_id=book_id)
    
    def by_user(self, user_id):
        return self.filter(user_id=user_id)