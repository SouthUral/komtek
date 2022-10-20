from django.contrib import admin
from .models import Handbook, VersionHandbook, Element

# Register your models here.
admin.site.register(Handbook)
admin.site.register(VersionHandbook)
admin.site.register(Element)
