from django.urls import path
from . import views
from .viewsets import UserListView

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_friend, name='add_friend'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/secrets/', views.add_secrets, name='secret-detail'),
    path('api/secrets/<int:secret_id>/', views.get_secrets, name='secret-detail'),
] 
