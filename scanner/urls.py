from django.urls import path
from scanner import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scan/', views.scan_view, name='scan'),
]
