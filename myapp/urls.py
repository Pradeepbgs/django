from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_home_page, name='get_home_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout')
]