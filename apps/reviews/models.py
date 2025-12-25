from django.db import models
from django.db.models import UniqueConstraint
from .managers import ReviewsManager

# Create your models here.
class Reviews(models.Model):
    user = models.ForeignKey(
        "users.Lectores", on_delete=models.CASCADE, related_name="reviews"
    )
    book = models.ForeignKey(
        "author_book.Book", on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reseñas"
        verbose_name = "reseña"
        verbose_name_plural = "reseñas"
        ordering = ["user", "book", "-created_at"]
        constraints = [
            UniqueConstraint(fields=["user", "book"], name="unique_user_book")
        ]
        
    object = ReviewsManager()

    def short_comment(self):
        if len(self.comment) <= 50:
            return self.comment
        else:
            return self.comment[:50]

    def __str__(self):
        return self.comment
