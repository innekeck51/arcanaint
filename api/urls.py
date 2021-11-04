from api.calories_mapping import CaloriesMapping
from api.climate import ClimateAnalyzer
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'regions', views.RegionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('regions/<int:id>/stations', views.StationView.as_view()),
    path('climate/excel', views.ClimateAnalyzeView.as_view()),
    path('lithology/classification', views.LithologyView.as_view()),
    path('calories-mapping', views.CaloriesMappingView.as_view()),
    path('ucg', views.UCGView.as_view()),
    path('preucg', views.PreUCGVIew.as_view()),
    path('astm', views.ASTMView.as_view())
]
