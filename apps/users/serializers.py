from rest_framework import serializers
from .models import Lectores

class LectorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lectores
        fields = ['username', 'email']
