from django.urls import path, include
from rest_framework import routers
from .views import HandbookAPView, ElementViewset, VerionViewset


router = routers.DefaultRouter()
router.register(r'handbooks', HandbookAPView)
router.register(r'elements', ElementViewset)
router.register(r'version', VerionViewset)


urlpatterns = router.urls