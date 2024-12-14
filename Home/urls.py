from django.urls import path
from . import views



urlpatterns = [
    path('', views.homepage),
    path('play2win.register/', views.register),
    path('play2win.rewards/', views.rewards),
    path('play2win.customer_service/', views.customer_service),
    path('play2win.games/', views.home_game)
]
