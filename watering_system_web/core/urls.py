from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pomiary/', views.pomiary, name='pomiary'),
    path('api/dane/', views.api_dane, name='api_dane'),
    path('podlej/', views.podlej, name='podlej'),
    path('obroc/', views.obroc, name='obroc'),
    path('ustaw_auto/toggle/', views.ustaw_auto_toggle, name='ustaw_auto_toggle'),
    path('zmierz/', views.zmierz, name='zmierz'),
]
