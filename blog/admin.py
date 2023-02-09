from django.contrib import admin

from blog.models import Post, Comment, CommentReply

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','created_by', 'created_at']

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post','commented_by', 'created_at']

    class Meta:
        model = Comment

admin.site.register(Comment, CommentAdmin)



class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ['id','post_comment','replied_by', 'created_at']

    class Meta:
        model = CommentReply

admin.site.register(CommentReply, CommentReplyAdmin)