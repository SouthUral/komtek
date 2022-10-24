from .models import Handbook, VersionHandbook, Element
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import HandbooksSerializer, ElementSerializer, VersionSerializer
import datetime


class HandbookAPView(viewsets.ModelViewSet):
    """
    По умолчанию возвращает список всех справочников
    """
    queryset = Handbook.objects.all()
    serializer_class = HandbooksSerializer


    @action(methods=['get'], detail=False)
    def get_on_date(self, request):
        """
        Метод возвращает список справочников актуальных на указанную дату
        принимаемые параметры: 'date' в формате '2020-10-10'
        """
        date_param = datetime.datetime.strptime(
                request.query_params.get('date'), "%Y-%m-%d"
            ).date()
        queryset = Handbook.objects.filter(version__date_start__lte=date_param).distinct('id')
        serializer = HandbooksSerializer(queryset, many=True)
        return Response({'refbooks':serializer.data})


class VerionViewset(viewsets.ModelViewSet):
    """
    Возвращет список всех версий
    """
    queryset = VersionHandbook.objects.all()
    serializer_class = VersionSerializer


class ElementViewset(viewsets.ModelViewSet):
    """
    По умолчанию возвращает список элементов всех справочников
    """
    queryset = Element.objects.all()
    serializer_class = ElementSerializer


    @action(methods=['get'], detail=False)
    def get_elements(self, request):
        """
        Возвращает список элементов справочника
        Если передан параметр id или title справочника - возвращает список элементов актуальной версии указанного справочника
        Если дополнительно передан параметр version - возвращает список элементов справочника указанной версии
        """
        queryset, version = self.get_queryset_elements(*self.getting_request_parameters(request))
        serializer = ElementSerializer(queryset, context={'request': request}, many=True)
        return Response({str(version): serializer.data})


    @action(methods=['get'], detail=False)
    def validate_elements(self, request):
        """
        Метод проверяет являются ли переданные параметры элементами указанного справочника
        Возвращает словарь с параметрами: {параметр: (True если элемент присутствует в справочнике) или False}
        Для выбора справочника используются параметры id или title
        С параметром 'version' проверка будет проводиться в справочнике указанной версии
        Без параметра 'version' проверка будет проведена в актуальной версии справочника
        """
        queryset, version = self.get_queryset_elements(*self.getting_request_parameters(request))
        response = dict()   
        items = {request.query_params.get(item) for item in request.query_params if item.startswith('p')}
        for item in items:
            response[item] = queryset.filter(value__iexact=item).exists()
        return Response({str(version): response})


    """пример для тестирования id=b3908710-c3f9-49c8-a299-011351e7931a, title=Врачи"""
    @staticmethod
    def get_queryset_elements(handbook_title, handbook_id, version):
        """
        Метод возвращает кортеж с queryset и version
        queryset с элементами выбранного справочника
        Если переданы handbook_title или handbook_id, возвращается queryset с 
        элементами актуального справочника.
        Если передан параметр version, возвращается queryset с элементами 
        выбранной версии справочника
        """
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
        """
        Метод достает из request параметры title, id, version и возвращает их в кортеже
        """
        handbook_title = request.query_params.get('title')
        handbook_id = request.query_params.get('id')
        version = request.query_params.get('version')
        return handbook_title, handbook_id, version
