from django.urls import path
from . import views



urlpatterns = [  # Example
    path('method/', views.payment),
    path('withdraw/', views.withdraw,)
]
