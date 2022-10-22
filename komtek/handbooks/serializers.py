from rest_framework import serializers
from .models import Handbook, VersionHandbook, Element


class HandbooksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Handbook
        fields = ('id', 'code', 'title')


class VersionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VersionHandbook
        fields = ('id', 'handbook', 'version', 'date_start')


class ElementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Element
        fields = ('id', 'version', 'code', 'value')
