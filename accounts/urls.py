from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_user, name='login'),  # Login page
    path('logout/', views.logout_user, name='logout'),  # Logout page
    

]
