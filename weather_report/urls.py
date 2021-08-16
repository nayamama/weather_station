from django.urls import path

from . import views

app_name = 'weather_report'

urlpatterns = [
    path('', views.index, name='home'),
    path('city/<str:city>/', views.detail, name='weather-detail'),
]
