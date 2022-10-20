from django.contrib import admin
from .models import Handbook, VersionHandbook, Element

# Register your models here.
class ElementInline(admin.TabularInline):
    model = Element
    fk_name = "version"


class HandbookAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'title')
    search_fields = ('code', 'title')


class VersionHandbookAdmin(admin.ModelAdmin):
    list_display = ('id', 'handbook', 'version', 'date_start')
    list_display_links = ('handbook', 'id')
    list_filter = ('handbook', 'version')
    inlines = [
        ElementInline,
    ]


class ElementAdmin(admin.ModelAdmin):
    list_display = ('id', 'version', 'code', 'value')
    list_display_links = ('version', 'id')
    list_filter = ('version',)


admin.site.register(Handbook, HandbookAdmin)
admin.site.register(VersionHandbook, VersionHandbookAdmin)
admin.site.register(Element, ElementAdmin)
