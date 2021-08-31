from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'regions', views.RegionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('regions/<int:id>/stations', views.StationView.as_view())
]
