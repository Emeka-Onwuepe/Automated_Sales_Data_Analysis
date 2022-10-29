from django.urls import path
from . import views

app_name="frontview"

urlpatterns = [
    path('',views.homeView,name='homeView'),
]