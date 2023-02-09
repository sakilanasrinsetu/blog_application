from dataclasses import field, fields
from .models import Post, Comment, CommentReply
from accounts.models import UserAccount
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from django.db.models import Q
from rest_framework import serializers, validators


class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        # fields = [
        #     'id',
        #     'username',
        #     'first_name',
        #     'last_name',
        #     'full_name',
        #     'email',
        #     'is_employee',
        #     'created_at',
        #     'updated_at'
        #     ]
        exclude = ['slug']