from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields=['name', 'nationality', 'birth_date', 'created_at']
        

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields=['title', 'author', 'publication_year', 'genre']