from rest_framework import serializers
from .models import Reviews

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields=['user', 'book', 'rating', 'rating', 'comment', 'created_at']
        
    def validate(self, data):
        user = data["user"]
        book = data["book"]
        
        if Reviews.objects.filter(user=user, book=book).exists():
            raise serializers.ValidationError(
                "Ya existe una reseña de este usuario para este libro."
            )
        return data