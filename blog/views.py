from django.shortcuts import render
from utils.custom_viewset import CustomViewSet

from .serializers import *
from utils.permissions import *

# Create your views here.


class PostViewSet(CustomViewSet):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        permission_classes = []
        if self.action in ["create","update", "destroy"]:
            permission_classes = [IsCustomAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            self.serializer_class = PostSerializer
        elif self.action == 'update':
            self.serializer_class = PostSerializer

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
        return ResponseWrapper(data=serializer.data, msg='Success',
                               status=200)

    def destroy(self, request, **kwargs):
        qs = self.queryset.filter(**kwargs).first()
        if not qs:
            return ResponseWrapper(error_msg='Post is Not Found',
                                   error_code=400, status=400)
        if not qs.created_by.username == request.user:
            return ResponseWrapper(error_msg='This is not Your Post',
                                   error_code=400, status=400)
        if qs:
            qs.delete()
            return ResponseWrapper(status=200, msg='deleted')
        else:
            return ResponseWrapper(error_msg="failed to delete",
                                   error_code=400)


class CommentViewSet(CustomViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailsSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        permission_classes = []
        if self.action in ["create", "update", "destroy"]:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            self.serializer_class = CommentSerializer
        elif self.action == 'update':
            self.serializer_class = CommentUpdateSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        post = request.data.get('post')
        if not post:
            return ResponseWrapper(error_msg='Post ID is Required', error_code=400, status=400)

        post_qs = Post.objects.filter(id = post).last()
        if not post_qs:
            return ResponseWrapper(error_msg='Post not Found', error_code=400, status=400)

        if serializer.is_valid():
            qs = serializer.save()
            qs.commented_by = request.user
            qs.save()
            serializer = CommentDetailsSerializer(instance=qs)
            return ResponseWrapper(data=serializer.data, msg='created')
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    def update(self, request, pk, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)

        comment_qs = self.queryset.filter(**kwargs)
        if not comment_qs.exists():
            return ResponseWrapper(error_code=400,
                                   error_msg='Comment Not Found', status=400)

        if serializer.is_valid():
            comment_qs = Comment.objects.filter(commented_by__username = request.user, id = pk).last()

            if not comment_qs:
                return ResponseWrapper(
                    error_msg="You Have Not Enough Permission to Edit This",
                    error_code=400,
                    status=400,
                )

            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = CommentDetailsSerializer(qs)
            return ResponseWrapper(data=serializer.data,
                                   msg='Update Successfully', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    def destroy(self, request, **kwargs):
        qs = self.queryset.filter(**kwargs).first()
        if not qs:
            return ResponseWrapper(error_msg='Comment is Not Found',
                                   error_code=400, status=400)
        if not qs.commented_by.username == request.user:
            return ResponseWrapper(error_msg='This is not Your Comment',
                                   error_code=400, status=400)
        if qs:
            qs.delete()
            return ResponseWrapper(status=200, msg='deleted')
        else:
            return ResponseWrapper(error_msg="failed to delete",
                                   error_code=400)

    def retrieve(self, request, pk, *args, **kwargs):
        qs = Comment.objects.filter(id=pk).last()
        if not qs:
            return ResponseWrapper(error_msg='Comment not Found',
                                   error_code=400, status=400)
        serializer = self.serializer_class(instance=qs)
        return ResponseWrapper(data=serializer.data, msg='Success',
                               status=200)

class CommentReplyViewSet(CustomViewSet):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplyDetailsSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        permission_classes = []
        if self.action in ["create", "update", "destroy"]:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            self.serializer_class = CommentReplySerializer
        elif self.action == 'update':
            self.serializer_class = CommentReplyUpdateSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        post_comment = request.data.get('post_comment')
        if not post_comment:
            return ResponseWrapper(error_msg='Comment ID is Required', error_code=400, status=400)

        comment_qs = Comment.objects.filter(id = post_comment).last()
        if not comment_qs:
            return ResponseWrapper(error_msg='Comment not Found', error_code=400, status=400)

        if serializer.is_valid():
            qs = serializer.save()
            qs.replied_by = request.user
            qs.save()
            serializer = CommentReplyDetailsSerializer(instance=qs)
            return ResponseWrapper(data=serializer.data, msg='created')
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    def update(self, request, pk, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)

        comment_qs = self.queryset.filter(**kwargs)
        if not comment_qs.exists():
            return ResponseWrapper(error_code=400,
                                   error_msg='Comment Not Found', status=400)

        if serializer.is_valid():
            comment_qs = Comment.objects.filter(commented_by__username = request.user, id = pk).last()

            if not comment_qs:
                return ResponseWrapper(
                    error_msg="You Have Not Enough Permission to Edit This",
                    error_code=400,
                    status=400,
                )

            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = CommentDetailsSerializer(qs)
            return ResponseWrapper(data=serializer.data,
                                   msg='Update Successfully', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    def destroy(self, request, **kwargs):
        qs = self.queryset.filter(**kwargs).first()
        if not qs:
            return ResponseWrapper(error_msg='Reply is Not Found',
                                   error_code=400, status=400)
        if not qs.replied_by.username == request.user:
            return ResponseWrapper(error_msg='This is not Your Reply',
                                   error_code=400, status=400)
        if qs:
            qs.delete()
            return ResponseWrapper(status=200, msg='deleted')
        else:
            return ResponseWrapper(error_msg="failed to delete",
                                   error_code=400)