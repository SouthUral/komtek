import datetime
import uuid

from rest_framework import viewsets
from rest_framework.exceptions import NotFound, ParseError, ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Element, Handbook, VersionHandbook
from .serializers import ElementSerializer, HandbooksSerializer, VersionSerializer


class HandbookAPView(viewsets.ModelViewSet):
    """
    По умолчанию возвращает список всех справочников
    """

    queryset = Handbook.objects.all()
    serializer_class = HandbooksSerializer

    @action(methods=["get"], detail=False)
    def get_on_date(self, request):
        """
        Метод возвращает список справочников актуальных на указанную дату
        принимаемые параметры: 'date' в формате '2020-10-10'
        """
        date_param = self.get_date(request)
        queryset = Handbook.objects.filter(
            version__date_start__lte=date_param
        ).distinct("id")
        serializer = self.serializer_class(queryset, many=True)
        return Response({"refbooks": serializer.data})

    @staticmethod
    def get_date(request):
        """
        метод корректность и наличие параметра date
        """
        date = request.query_params.get("date")
        if not date:
            raise ParseError({"error": "недостаточно параметров для запроса"})
        try:
            return datetime.datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError({"error": "неверный формат даты"})


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

    @action(methods=["get"], detail=False)
    def get_elements(self, request):
        """
        Возвращает список элементов справочника
        Если передан параметр id или title справочника - возвращает список элементов актуальной версии указанного справочника
        Если дополнительно передан параметр version - возвращает список элементов справочника указанной версии
        """
        queryset, version = self.get_queryset_elements(
            *self.getting_request_parameters(request)
        )
        serializer = ElementSerializer(
            queryset, context={"request": request}, many=True
        )
        return Response({str(version): serializer.data})

    @action(methods=["get"], detail=False)
    def validate_elements(self, request):
        """
        Метод проверяет являются ли переданные параметры элементами указанного справочника
        Возвращает словарь с параметрами: {параметр: (True если элемент присутствует в справочнике) или False}
        Для выбора справочника используются параметры id или title
        С параметром 'version' проверка будет проводиться в справочнике указанной версии
        Без параметра 'version' проверка будет проведена в актуальной версии справочника
        """
        queryset, version = self.get_queryset_elements(
            *self.getting_request_parameters(request)
        )
        response = dict()
        items = {
            request.query_params.get(item)
            for item in request.query_params
            if item.startswith("p")
        }
        for item in items:
            response[item] = queryset.filter(value__iexact=item).exists()
        return Response({str(version): response})

    @classmethod
    def get_queryset_elements(
        cls, handbook_title: str, handbook_id: str, version: str
    ) -> tuple:
        """
        Метод возвращает кортеж с queryset и version
        queryset с элементами выбранного справочника
        Если переданы handbook_title или handbook_id, возвращается queryset с
        элементами актуального справочника.
        Если передан параметр version, возвращается queryset с элементами
        выбранной версии справочника
        """
        v_handbook = cls.get_handbook(handbook_title, handbook_id)
        if not v_handbook.exists():
            raise NotFound({"error": "Указанный справочник не найден"})
        handbook_version = cls.get_version(v_handbook, version)
        if handbook_version:
            queryset = handbook_version.elements.all()
            return queryset, handbook_version
        raise NotFound({"error": "Указанная версия не найдена"})

    @staticmethod
    def getting_request_parameters(request):
        """
        Метод достает из request параметры title, id, version и возвращает их в кортеже
        """
        handbook_title = request.query_params.get("title")
        handbook_id = request.query_params.get("id")
        version = request.query_params.get("version")
        return handbook_title, handbook_id, version

    @staticmethod
    def get_version(v_handbook, version=None):
        if version:
            return v_handbook.filter(version=version).last()
        date_now = datetime.datetime.now().date()
        return v_handbook.filter(date_start__lte=date_now).last()

    @staticmethod
    def get_handbook(handbook_title, handbook_id):
        if handbook_title:
            return VersionHandbook.objects.filter(handbook__title=handbook_title)
        if handbook_id:
            try:
                id = uuid.UUID(handbook_id)
            except ValueError:
                raise ValidationError({"error": "неверный UUID"})
            return VersionHandbook.objects.filter(handbook__id=id)
        raise ParseError({"error": "недостаточно параметров для запроса"})
