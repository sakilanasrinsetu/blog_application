from django.urls import path
from .views import *


urlpatterns = [
    path('register/',
         UserAccountViewSet.as_view({'post': 'register'},
                                    name='register')),

    path('login/',
         UserAccountViewSet.as_view({'post': 'login'},
                                    name='login')),

    path('user_details/',
         UserAccountViewSet.as_view({'get': 'user_details'},
                                    name='user_details')),
    path('user/',
         UserAccountViewSet.as_view({'get': 'user_list'},
                                    name='user')),
    path('employee_create/',
         UserAccountViewSet.as_view({'post': 'employee_create'},
                                    name='employee_create')),
    path('profile_update/<pk>/',
         UserAccountViewSet.as_view({'post': 'profile_update'},
                                    name='profile_update')),
    path('user_delete/<pk>/',
         UserAccountViewSet.as_view({'delete': 'destroy'},
                                    name='user_delete')),

]