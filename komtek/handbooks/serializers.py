from dataclasses import field
from rest_framework import serializers
from .models import Handbook


class HandbooksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Handbook
        fields = ('id', 'code', 'title', 'description')


# class VersionSerializer(serializers.HyperlinkedModelSerializer):
#     handbook = serializers.CharField()
#     version = serializers.CharField(max_length=50)
#     date_start = serializers.DateField()


# class ElementSerializer(serializers.HyperlinkedModelSerializer):
#     version = serializers.CharField()
#     code = serializers.CharField(max_length=100)
#     value = serializers.CharField()