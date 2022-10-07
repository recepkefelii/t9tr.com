from rest_framework import serializers
from .models import url

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = url
        fields = ['id','url']



