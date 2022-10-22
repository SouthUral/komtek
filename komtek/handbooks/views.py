from django.shortcuts import render
from .models import Handbook, VersionHandbook, Element
from rest_framework.views import APIView
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import HandbooksSerializer, ElementSerializer
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
        queryset = Handbook.objects.filter(versionhandbook__date_start__lte=date_param)
        serializer = HandbooksSerializer(queryset, many=True)
        return Response({'refbooks':serializer.data})


class ElementAPView(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
