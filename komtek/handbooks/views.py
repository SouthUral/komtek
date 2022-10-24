# from django.shortcuts import render
from ensurepip import version
from .models import Handbook, VersionHandbook, Element
from rest_framework import viewsets
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


class ElementViewset(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    

    @action(methods=['get'], detail=False)
    def get_elements(self, request):
        queryset, version = self.get_queryset_elements(*self.getting_request_parameters(request))
        serializer = ElementSerializer(queryset, context={'request': request}, many=True)
        return Response({str(version): serializer.data})

    
    @action(methods=['get'], detail=False)
    def validate_elements(self, request):
        queryset, version = self.get_queryset_elements(*self.getting_request_parameters(request))
        response = dict()   
        items = {request.query_params.get(item) for item in request.query_params if item.startswith('p')}
        for item in items:
            response[item] = queryset.filter(value__iexact=item).exists()
        return Response({str(version): response})



    """пример для тестирования id=b3908710-c3f9-49c8-a299-011351e7931a, title=Врачи"""
    @staticmethod
    def get_queryset_elements(handbook_title, handbook_id, version):
        if handbook_title:
            v_handbook = VersionHandbook.objects.filter(handbook__title=handbook_title)
        elif handbook_id:
            v_handbook = VersionHandbook.objects.filter(handbook__id=handbook_id)
        else:
            return Response('not enough parameters to form the request')
        if version:
            version = v_handbook.get(version=version)
            queryset = version.elements.all()
        else:
            date_now = datetime.datetime.now().date()
            version = v_handbook.filter(date_start__lte=date_now).last()
            queryset = version.elements.all()
        return queryset, version


    @staticmethod
    def getting_request_parameters(request):
        """необходимо сделать проверку, есть ли неободимо количество параметров для
        формирования ответа
        """
        handbook_title = request.query_params.get('title')
        handbook_id = request.query_params.get('id')
        version = request.query_params.get('version')
        return handbook_title, handbook_id, version
