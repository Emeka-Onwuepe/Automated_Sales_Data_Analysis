from django.urls import path
from . import views

app_name="process"

urlpatterns = [
    path('<str:user_id>/<str:dataset_id>',views.ClassifyView,name='classifyView'),
    path('<str:user_id>/<str:dataset_id>/process',views.AnalysisView,name='analysisView'),
]