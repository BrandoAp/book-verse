from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ReviewsSerializer
from .models import Reviews

# Create your views here.
class CreateReviewApiView(APIView):
    """
    Vista para crear una nueva review
    """
    def post(self, request):
        serializer = ReviewsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class ListReviewsApiView(APIView):
    """
    Vista para listar todas las reviews
    """
    def get(self, request):
        query = Reviews.objects.all()
        serializer = ReviewsSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RetriveReviewsApiView(APIView):
    """
    Vista para obtener una review por el id
    """    
    def get(self, request, pk):
        try:
            query = Reviews.objects.get(id=pk)
            
        except Reviews.DoesNotExist as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            
        serializer = ReviewsSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UpdateReviewApiView(APIView):
    """
    Vista para actualizar una review
    """
    def update(self, request, pk):
        try:
            review = Reviews.objects.get(id=pk)
        
        except Reviews.DoesNotExist as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            
        serializer = ReviewsSerializer(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class DeleteReviewApiView(APIView):
    """
    Vista para eliminar una review
    """    
    def delete(self, request, pk):
        try:
            review = Reviews.objects.get(id=pk)
        
        except Reviews.DoesNotExist as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ReviewsByBookApiView(APIView):
    """
    Vista para obtener las reviews de un libro por su id
    """
    def get(self, request, book_id):
        try:
            query = Reviews.object.by_book(book_id)
        except Reviews.DoesNotExist as e:
            return Response({
                "not_found": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            
        serializer = ReviewsSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ReviewsByUserAPIView(APIView):
    """
    Vista para obtener las reviews de un usuario a un libro por su id
    """
    def get(self, request, user_id):
        try:
            query = Reviews.object.by_user(user_id)
        except Reviews.DoesNotExist as e:
            return Response({
                "not_found" : str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            
        serializer = ReviewsSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)