from django.shortcuts import render
from .models import Handbook, VersionHandbook, Element
from rest_framework.views import APIView
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from .serializers import HandbooksSerializer


# Create your views here.
class HandbookAPView(viewsets.ModelViewSet):
    queryset = Handbook.objects.all()
    serializer_class = HandbooksSerializer
    permission_classes = [permissions.IsAuthenticated]
