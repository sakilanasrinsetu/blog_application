from django.shortcuts import render
from requests import request

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from .serializers import RegisterSerializer
from utils.custom_viewset import CustomViewSet
# from utils.custom_permissions import *
from accounts.models import UserAccount
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, status, viewsets

from django.utils import timezone
from drf_yasg2.utils import swagger_auto_schema
from django.contrib.auth import get_user_model, login
import random
from accounts.serializers import *
from utils.response_wrapper import ResponseWrapper
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password


# Create your views here.

class UserAccountViewSet(CustomViewSet):
    queryset = UserAccount.objects.all()
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
        if self.action == 'register':
            self.serializer_class = RegisterSerializer

        elif self.action == 'login':
            self.serializer_class = AuthTokenSerializer

        else:
            self.serializer_class = AuthTokenSerializer

        return self.serializer_class

    def register(self, request, *args, **kwargs):
        password = request.data.pop("password")
        email = request.data["email"]
        username = request.data["username"]

        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        full_name = str(first_name) + ' ' + str(last_name)

        email_exist = UserAccount.objects.filter(email=email).exists()

        if email_exist:
            return ResponseWrapper(
                error_msg="Email is Already Used", status=400
            )

        username_exist = UserAccount.objects.filter(username=username).exists()

        if username_exist:
            return ResponseWrapper(
                error_msg="Username is Already Used", status=400
            )
        try:
            password = make_password(password=password)
            user = UserAccount.objects.create(
                full_name=full_name,
                password=password,
                **request.data
            )
            _, token = AuthToken.objects.create(user)
        except Exception as err:
            # logger.exception(msg="error while account cration")
            return ResponseWrapper(
                error_msg="Account Can't Create", status=400
            )

        serializer = UserProfileDetailSerializer(instance=user)

        context = {
            'user_info': serializer.data,
            'token': token,
        }
        return ResponseWrapper(data=context, status=200)

    def login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        qs = UserAccount.objects.filter(Q(username=username)| Q(email=username)
                                        ).last()
        if not qs:
            return ResponseWrapper(error_msg='Username is Not Valid', status=400)

        elif qs.check_password(password):
            _, token = AuthToken.objects.create(qs)
            serializer = UserProfileDetailSerializer(instance=qs)

            context = {
                'user_info': serializer.data,
                'token': token,
            }
            return ResponseWrapper(data=context, status=200)

        return ResponseWrapper(error_msg='Password is Not Valid', status=400)

    def user_details(self, request, *args, **kwargs):
        qs = UserAccount.objects.filter(username=self.request.user).last()

        if not qs:
            return ResponseWrapper(error_msg='This is Not Your Account',
                                   error_code=400)

        serializer = UserProfileDetailSerializer(instance=qs)


        return ResponseWrapper(data=serializer.data, status=200)