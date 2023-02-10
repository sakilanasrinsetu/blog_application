from django.urls import path
from .views import *


urlpatterns = [
    path('post/',
         PostViewSet.as_view({'get': 'list', 'post':'create'},
                             name='post')),
    path('post/<pk>/',
         PostViewSet.as_view({'patch': 'update', 'get': 'retrieve',
                              'delete':'destroy'}, name='post')),
    path('comment/',
         CommentViewSet.as_view({'get': 'list', 'post':'create'},
                                name='comment')),
    path('comment/<pk>/',
         CommentViewSet.as_view({'patch': 'update', 'get': 'retrieve',
                                 'delete':'destroy'}, name='comment')),
    path('comment_reply/',
         CommentReplyViewSet.as_view({'get': 'list', 'post':'create'},
                                     name='comment_reply')),
    path('comment_reply/<pk>/',
         CommentReplyViewSet.as_view({'patch': 'update', 'get': 'retrieve',
                                      'delete':'destroy'}, name='comment_reply')),
]