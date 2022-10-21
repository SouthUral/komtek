from django.urls import path
from .views import HandbookAPView



urlpatterns = [
    path('api/', HandbookAPView.as_view()),
]