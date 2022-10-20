from django.db import models


# Create your models here.
class Handbook(models.Model):
    """Модель справочника"""
    identifier = models.UUIDField(verbose_name='Идентификатор')
    code = models.CharField(max_length=100, verbose_name='код', unique=True)
    title = models.CharField(max_length=300, verbose_name='наименование справочника')
    description = models.TextField(verbose_name='описание', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'


class VersionHandbook(models.Model):
    """Модель версии справочника"""
    identifier = models.UUIDField(verbose_name='Идентификатор')
    id_handbook = models.ForeignKey(Handbook, on_delete=models.CASCADE)
    version = models.CharField(max_length=50, verbose_name='версия')
    """Дата старта устанавливается во время создания версии"""
    date_start = models.DateField(verbose_name='Дата начала действия версии')

    def __str__(self):
        return f'{self.version}: {self.date_start}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        """Установлены ограничения на уникальность полей в одной таблице"""
        constraints = [
            models.UniqueConstraint(fields=['id_handbook', 'version', 'date_start'], name='unique_version')
            ]


class Element(models.Model):
    """Модель элемента справочника"""
    identifier = models.UUIDField(verbose_name='Идентификатор')
    id_version = models.ForeignKey(VersionHandbook, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, verbose_name='код')
    value = models.CharField(max_length=300, verbose_name='значение элемента')

    def __str__(self):
        return f'{self.id_version}: {self.value}'

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'
        """Установлены ограничения на уникальность полей в одной таблице"""
        constraints = [
            models.UniqueConstraint(fields=['id_version', 'code'], name='unique_element')
            ]