from django.urls import path, include
from . import views, viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = 'tegakinum'
urlpatterns = [
    path('', include(router.urls)),
    path('predict/', views.PredictView.as_view(), name='predict'),
]
