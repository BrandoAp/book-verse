from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

"""
Author EndPoints
"""
class CreateAuthorApiView(APIView):
    """ 
    Vista para crear un nuevo autor.
    /api/authors/created/ 
    """
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListAuthorApiView(APIView):
    """ 
    Vista para listar todos los autores. 
    /api/authors/ 
    """
    def get(self, request):
        authores = Author.objects.list_authors()
        serializer = AuthorSerializer(authores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
class ListAuthorByIdApiView(APIView):
    """ 
    Vista para buscar un autor por Id. 
    /api/authors/by-id/?id=1 
    """
    def get(self, request):
        author_id = request.query_params.get('id', '').strip()  
        
        if not author_id:
            return Response({
                "error": "falta el parametro { id } en la solicitud"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:    
            author = Author.objects.list_by_id(author_id)
        except Author.DoesNotExist:
            return Response({
                "no encontrado" : f"El autor con id { author_id } no existe"
            }, status=status.HTTP_404_NOT_FOUND)
            
        return Response({
            'nombre': author.name,
            'nacionalidad': author.nationality,
            'fecha de cumpleaños': author.birth_date,
            'fecha de creación': author.created_at
        }, status=status.HTTP_200_OK)
        
               
class AuthorWithMinBooksApiView(APIView):
    """ 
    Vista para obtener autores con al menos 5 libros. 
    /api/authors/with-books/?id=1
    """
    def get(self, request):
        
        pk = request.query_params.get('id', '').strip()

        if not pk:
            return Response({
                'error': 'El parametro { id } esta vacio'
            }, status=status.HTTP_400_BAD_REQUEST)
              
        try:
            books = Author.objects.with_min_books(pk)
        except ValueError as e:
            return Response({
                "no encontrado": f"{str(e)}"
            }, status=status.HTTP_404_NOT_FOUND)
        
        if books is None:
            return Response({
                "error": f"El autor con id '{ pk }' no tiene 5 o mas libros registrados"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "books": f"El autor con id '{ pk }' tiene {books} libros registrados"
        }, status=status.HTTP_200_OK)
        

class AuthorTotalBooksApiView(APIView):
    """
    Vista para obtener todos los libros de un autor. 
    /api/authors/total-books/?id=1
    """
    def get(self, request):
        author_id = request.query_params.get('id', '').strip()
        
        if not author_id:
            return Response({
                "error": "El parametro { id } esta vacio"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:    
            book_for_author = Author.total_book_for_author(self, pk=author_id)
        except ValueError as e:
            return Response({
                "no encontrado": f"{str(e)}"
            }, status=status.HTTP_404_NOT_FOUND)
            
        return Response({
            "total" : f"Este autor tiene {book_for_author} libros"
        }, status=status.HTTP_200_OK)
        
"""
class AuthorUpdateApiView(APIView):

    Vista para actualizar un autor por el id
    /api/authors/update/?id=1
    
    def update(self, request):
        pk = request.query_params.get('id', '').strip()
        
        if not pk:
           return Response({
                "error": "El parametro id no puede estar vacio y es obligatorio"
            }, status=status.HTTP_400_BAD_REQUEST)
"""
        
        
class AuthorDeleteApiView(APIView):
    """
    Vista para eliminar un autor por id.
    /api/authors/delete/1/
    """
    def delete(self, request, pk):
        
        try:    
            author = Author.objects.get(id=pk)
        except Author.DoesNotExist as e:
            return Response({
                "no encontrado": f"No existe el autor con el id: '{pk}' no existe. {str(e)}"
            }, status=status.HTTP_404_NOT_FOUND)
            
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    


"""
Books EndPoints
"""     
class CreateBookApiView(APIView):
    """
    Vista para crear nuevos libros
    /api/books/
    """
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListBooksApiView(APIView):
    """
    Vista para listar todos los libros
    /api/books/list/
    """  
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class RetrieveBooksApiView(APIView):
    """
    Vista para busqueda de libros por su id
    /api/books/by-id/
    """
    def get(self, request):
        pk = request.query_params.get('id', '').strip()
        
        if not pk:
            return Response({
                "error": "El parametro { id } no puede estar vacio"
            }, status=status.HTTP_400_BAD_REQUEST)
          
            
        try:
            query = Book.objects.get(id=pk)
        except Book.DoesNotExist as e:
            return Response({
                "error": f"{str(e)}"
            }, status=status.HTTP_404_NOT_FOUND)
            
        return Response({
            'title': query.title,
            'author': query.author.name,
            'publication_year': query.publication_year,
            'genero': query.genre,  
            'created_at': query.created_at
        }, status=status.HTTP_200_OK)
        
        
class BookFilterByGenreApiView(APIView):
    """
    Vista para filtrado de libros por su genero
    /api/books/by-genre/
    """
    def get(self, request):
        genre = request.query_params.get('genre', '').strip()
        
        if not genre:
            return Response({
                "error": "parametro { genre } no puede estar vacio"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            query = Book.objects.filter_by_genre(genre)
        except ValueError as e:
            return Response({
                "not_found": f'{str(e)}'
            }, status=status.HTTP_404_NOT_FOUND)
            
        serializer = BookSerializer(query, many=True)
        
        return Response({
            "books": serializer.data
        }, status=status.HTTP_200_OK)
        
        
class BookAverageRatingApiView(APIView):
    """
    Vista para obtener el rating de un libro
    /api/books/rating/<int:pk>/
    """
    def get(self, request, pk):
        try:
            rating = Book.average_rating(self, pk)
        except ValueError as e:
            return Response({
                "not_found": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            
        return Response(rating, status=status.HTTP_200_OK)
    
class BookDeleteApiView(APIView):
    """
    Vista para eliminar un libro
    /api/books/delete/<int:pk>/
    """
    def delete(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response({
                "error": f"no existe un libro con id { pk }"
            }, status=status.HTTP_404_NOT_FOUND)
        
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)