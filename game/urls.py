from django.urls import path
from . import views



urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('flappybet/', views.flappy_game, name='flappy_game'),
    path('flappybet.icons/', views.game_icons, name='game_icons'),
    path('flappybet.referal/', views.referal, name='referal'),
    path('flappybet.spin/', views.scatter, name="scatter"),

  
]
