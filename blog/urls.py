from django.urls import path
from .views import *


urlpatterns = [
    path('post/',
         PostViewSet.as_view({'get': 'list', 'post':'create'}, name='post')),
    path('post/<pk>/',
         PostViewSet.as_view({'post': 'update', 'get': 'retrieve', 'delete':'destroy'}, name='post')),
]