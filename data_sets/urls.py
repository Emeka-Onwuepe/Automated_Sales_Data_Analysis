from django.urls import path
from . import views

app_name="process"

urlpatterns = [
    path('<str:dataset_id>',views.ClassifyView,name='classifyView'),
    path('<str:dataset_id>/process',views.AnalysisView,name='analysisView'),
    path('data/dashboard',views.dashboardView,name='dashboardView'),
    path('delete/<int:dataset_id>',views.deleteView,name='deleteview'),
]