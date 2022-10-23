from multiprocessing import context
from urllib.request import Request
from django.shortcuts import render
from .models import Handbook, VersionHandbook, Element
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import HandbooksSerializer, ElementSerializer, VersionSerializer
import datetime


# Create your views here.
class HandbookAPView(viewsets.ModelViewSet):
    queryset = Handbook.objects.all()
    serializer_class = HandbooksSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def get_on_date(self, request):
        date_param = datetime.datetime.strptime(
                request.query_params.get('date'), "%Y-%m-%d"
            ).date()
        queryset = Handbook.objects.filter(version__date_start__lte=date_param).distinct('id')
        serializer = HandbooksSerializer(queryset, many=True)
        return Response({'refbooks':serializer.data})


class VerionViewset(viewsets.ModelViewSet):
    queryset = VersionHandbook.objects.all()
    serializer_class = VersionSerializer

    @action(methods=['get'], detail=False)
    def get_elements(self, request):
        date_now = datetime.datetime.now().date()
        handbook = request.query_params.get('title')
        version_handbook = VersionHandbook.objects.filter(handbook__title=handbook, date_start__lte=date_now).last()
        queryset = version_handbook.elements.all()
        serializer = ElementSerializer(queryset, many=True)
        return Response({'elements': serializer.data})


class ElementViewset(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    

    @action(methods=['get'], detail=False)
    def get_elements(self, request):
        if request.query_params.get('title'):
            handbook = request.query_params.get('title')
            versions_handbook = VersionHandbook.objects.filter(handbook__title=handbook)
            if request.query_params.get('version'):
                version_handbook = request.query_params.get('version')
                queryset = versions_handbook.get(version=version_handbook).elements.all()
            else:
                date_now = datetime.datetime.now().date()
                version_handbook = versions_handbook.filter(date_start__lte=date_now).last()
                queryset = version_handbook.elements.all()
            serializer = ElementSerializer(queryset, context={'request': request}, many=True)
            return Response({str(version_handbook): serializer.data})
        else:
            return Response('parameters not passed')

