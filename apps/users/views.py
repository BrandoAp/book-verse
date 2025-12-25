from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Lectores
from .serializers import LectorSerializers

# Create your views here.
class CreateLectorApiView(APIView):
    """
    Vista para crear un nuevo lector.
    /api/lector/created/
    """
    def post(self, request):
        serialiazer = LectorSerializers(data=request.data)
        serialiazer.is_valid(raise_exception=True)
        serialiazer.save()
        return Response(serialiazer.data, status=status.HTTP_201_CREATED)
    
    
class ListLectoresApiView(APIView):
    """
    Vista para listar todos los lectores.
    /api/lector/
    """
    def get(self, request):
        lectores = Lectores.objects.all()
        serializer = LectorSerializers(lectores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
   
class RetrieveLectorApiView(APIView):
    """ 
    Vista para obtener un lector por id.
    /api/lector/<int:pk>/
    """
    def get(self, request, pk):
        try:
            lector = Lectores.objects.get(id=pk)
        except Lectores.DoesNotExist as e:
            return Response({
                "not_found" : str(e)
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LectorSerializers(lector)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UpdateLectorApiView(APIView):
    """
    Vista para actualizar un lector.
    /api/lector/update/<int:pk>/
    """
    def update(self, request, pk):
        try:
            lector = Lectores.objects.get(id=pk)
        except Lectores.DoesNotExist as e:
            return Response({
                "not_found": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            
        serializer = LectorSerializers(lector, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
   
class DeleteLectorApiView(APIView):
    """
    Vista para eliminar un lector por id.
    /api/lector/delete/<int:pk>/
    """
    def delete(self, request, pk):
        try:
            lector = Lectores.objects.get(id=pk)
        except Lectores.DoesNotExist as e:
            return Response({
                "not_found": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            
        lector.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
  
class TotalLectorReviewApiView(APIView):
    """
    Vista para obtener el total de reviews de un lector
    /api/lector/review/?id=pk
    """
    def get(self, request):
        pk = request.query_params.get('id', '').strip()
        
        if not pk:
            return Response({
                "error": "El paramatro { id } no puede estar vacio"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            query = Lectores.total_reviews_for_lector(self, pk)
        except ValueError as e:
            return Response({
                "not_found": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            
        return Response({
            "total_review": query
        }, status=status.HTTP_200_OK)
        
        
class LectorActiveForYear(APIView):
    """
    Vista para obtener a lectores activos desde un año especifico
    /api/lector/active?year=2003
    """
    def get(self, request):
        year = request.query_params.get('year', '').strip()
        
        if not year:
            return Response({
                "error": "El parametro { year } no puede estar vacio o hace falta"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:        
            query = Lectores.objects.active_since(year)
        except ValueError as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if not query.exists():
            return Response({
                "not_found": f"No existe ningun lector activo desde el año { year }"
            }, status=status.HTTP_404_NOT_FOUND)
            
        serializer = LectorSerializers(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)