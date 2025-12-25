from django.db import models
from django.db.models import UniqueConstraint, Avg
from .managers import AuthorManager, BookManager

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)
    nationality = models.CharField(max_length=50)
    birth_date = models.DateField(auto_now_add=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = AuthorManager()
    
    class Meta:
        db_table='autores'
        verbose_name='autor'
        verbose_name_plural='autores'
        ordering=['name']
        
    def total_book_for_author(self, pk):
        try:
            books_for_author = Author.objects.get(id=pk)
        except Author.DoesNotExist as e:
            raise ValueError(f"El author con id { pk } no existe {str(e)}")
        return books_for_author.books.count()
        
    def __str__(self):  
        return self.name 

class Book(models.Model):                
    title = models.CharField(max_length=50)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
    )
    publication_year = models.PositiveIntegerField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = BookManager()
    
    class Meta:
        verbose_name='libro'
        verbose_name_plural='libros'
        ordering=['created_at']
        constraints=[
            UniqueConstraint(fields=['title', 'author'], name='unique_author_book')
        ]
        
    def average_rating(self, pk):
        try:
            average_for_book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            raise ValueError(f"no existe el libro con id {pk}")
        return average_for_book.reviews.all().aggregate(Avg('rating'))
    
    def __str__(self):
        return f"{self.title}: {self.author}"
    