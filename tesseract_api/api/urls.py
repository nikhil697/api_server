from django.urls import path
from .views import get_text, get_bboxes

urlpatterns = [
    path('get-text/', get_text, name='get_text'),
    path('get-bboxes/', get_bboxes, name='get_bboxes'),
]