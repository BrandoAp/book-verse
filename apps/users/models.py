from django.db import models
from .managers import *

# Create your models here.
class Lectores(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    objects = LectoresManagers()
    
    class Meta:
        db_table='lectores'
        verbose_name='lector'
        verbose_name_plural='lectores'
        ordering=['-joined_at']
        
    def total_reviews_for_lector(self, pk):
        try:
            total = Lectores.objects.get(id=pk)
        except Lectores.DoesNotExist as e:
            raise ValueError(str(e))
        
        return total.reviews.count()
        
    def __str__(self):
        return self.username