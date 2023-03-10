from dataclasses import field, fields
from .models import Post, Comment, CommentReply
from accounts.models import UserAccount
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from django.db.models import Q
from rest_framework import serializers, validators
from accounts.serializers import UserProfileDetailSerializer


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'featured_image',
            'description',
            'created_by',
            'created_at',
            'updated_at',
                  ]

    def get_created_by(self, obj):
        if obj.created_by:
            serializer = UserProfileDetailSerializer(instance = obj.created_by)
            return serializer.data
        return None


class PostSerializer(serializers.ModelSerializer):
    featured_image = Base64ImageField()

    class Meta:
        model = Post
        exclude = ['slug','created_by']

    def create(self, validated_data):
        featured_image = validated_data.pop('featured_image', None)
        if featured_image:
            return Post.objects.create(featured_image=featured_image, **validated_data)
        return Post.objects.create(**validated_data)


class CommentDetailsSerializer(serializers.ModelSerializer):
    commented_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'comment',
            'commented_by',
            'created_at',
            'updated_at'
        ]

    def get_commented_by(self, obj):
        if obj.commented_by:
            serializer = UserProfileDetailSerializer(instance = obj.commented_by)
            return serializer.data
        return None


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ['commented_by']


class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ['commented_by', 'post']


class CommentReplyDetailsSerializer(serializers.ModelSerializer):
    replied_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CommentReply
        fields = [
            'id',
            'reply',
            'post_comment',
            'replied_by',
            'created_at',
            'updated_at'
        ]

    def get_replied_by(self, obj):
        if obj.replied_by:
            serializer = UserProfileDetailSerializer(instance=obj.replied_by)
            return serializer.data
        return None


class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        # fields = '__all__'
        exclude = ['replied_by']


class CommentReplyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        # fields = '__all__'
        exclude = ['replied_by', 'post_comment']