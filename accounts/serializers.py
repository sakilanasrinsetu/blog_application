from dataclasses import field, fields
from .models import *
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from django.db.models import Q
from rest_framework import serializers, validators


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserAccount
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            ]


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = [
            'first_name',
            'last_name',
            'email'
            ]

class UserProfileDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'is_employee',
            'created_at',
            'updated_at'
            ]


class EmployeeCreateSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=UserAccount.objects.all()
    )

