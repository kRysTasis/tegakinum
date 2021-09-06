from django.urls import path, include
from . import views, viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('predict', viewsets.PredictViewSet)

app_name = 'tegakinum'
urlpatterns = [
    path('', include(router.urls)),
]
