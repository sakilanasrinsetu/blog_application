from django.shortcuts import render
from requests import request

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from .serializers import *
from utils.custom_viewset import CustomViewSet
# from utils.custom_permissions import *
from accounts.models import UserAccount
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, status, viewsets

from django.utils import timezone
from drf_yasg2.utils import swagger_auto_schema
from django.contrib.auth import get_user_model, login
import random
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.response_wrapper import ResponseWrapper

# Create your views here.

class PostViewSet(CustomViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        permission_classes = []
        if self.action in ["user_details"]:
            permission_classes = [IsAuthenticated]
        # else:
        #     # permissions.DjangoObjectPermissions.has_permission()
        #     permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        # if self.action == 'register':
        #     self.serializer_class = RegisterSerializer

        # elif self.action == 'login':
        #     self.serializer_class = AuthTokenSerializer

        # else:
        #     self.serializer_class = AuthTokenSerializer

        return self.serializer_class


    # def 