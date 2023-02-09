from django.urls import path
from .views import *


urlpatterns = [
    path('post/',
         PostViewSet.as_view({'get': 'list'}, name='post')),
]