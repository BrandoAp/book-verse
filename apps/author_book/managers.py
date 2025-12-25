from django.db import models

class AuthorManager(models.Manager):
    
    def list_authors(self):
        authores = self.all()
        return authores
    
    def list_by_id(self, pk=None):
        return self.get(id=pk)
    
    def with_min_books(self, pk=None):
        try:
            author = self.get(id=pk)
        except self.model.DoesNotExist:
            raise ValueError(f"El author con id {pk} no existe.")
        
        num_libros = author.books.all().count()
        if num_libros >= 5:
            return num_libros


class BookManager(models.Manager):
    
    def filter_by_genre(self, genre):
        books = self.filter(genre__icontains=genre)
        
        if not books.exists():
            raise ValueError(f'No existe el genero: {genre}')
            
        return books
    
    def recent_books(self):
        return self.filter(publication_year__lte=5)