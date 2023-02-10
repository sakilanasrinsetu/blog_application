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
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        permission_classes = []
        if self.action in ["create","update"]:
            permission_classes = [IsAuthenticated]
        # else:
        #     # permissions.DjangoObjectPermissions.has_permission()
        #     permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            self.serializer_class = PostCreateSerializer
        elif self.action == 'update':
            self.serializer_class = PostCreateSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        title = request.data.get('title')
        post_qs = Post.objects.filter(title = title).last()
        if post_qs:
            return ResponseWrapper(error_msg='Post is Already Found', error_code=400, status=400)
        if serializer.is_valid():
            qs = serializer.save()
            qs.created_by = request.user
            qs.save()
            serializer = self.serializer_class(qs)
            return ResponseWrapper(data=serializer.data, msg='created')
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    def update(self, request, pk, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)

        post_qs = self.queryset.filter(**kwargs)
        if not post_qs.exists():
            return ResponseWrapper(error_code=400,
                                   error_msg='Post Not Found', status=400)

        if serializer.is_valid():
            title = serializer.validated_data.get("title")

            if self.get_queryset().filter(title__iexact=title).exclude(id=pk).exists():
                return ResponseWrapper(
                    error_msg="Post title Already Exists",
                    error_code=400,
                    status=400,
                )

            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = PostDetailSerializer(qs)
            return ResponseWrapper(data=serializer.data, msg='Update Successfully', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    def retrieve(self, request, pk, *args, **kwargs):
        qs = Post.objects.filter(Q(slug= pk) or Q(id = pk)).last()
        if not qs:
            return ResponseWrapper(error_msg='Post not Found', error_code=400, status=400)
        serializer = self.serializer_class(instance=qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)