from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('all-post/', views.get_all_post, name='get_all_posts'),
    path('delete/', views.delete_post, name='delete_post'),
]
