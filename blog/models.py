from django.db import models
from accounts.models import UserAccount
from django.utils.text import slugify

# Create your models here.



class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="title")
    slug = models.SlugField(blank=True, unique=True)
    featured_image = models.FileField(
        blank=True, null=True, upload_to='post'
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )
    created_by = models.ForeignKey(UserAccount, on_delete=models.CASCADE,
                                   related_name="posts", null=True, blank=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='updated at'
    )

    def __str__(self):
        return self.title

    def generate_slug(self):
        return slugify(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    commented_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name='comments',
        null=True, blank=True
    )
    comment = models.TextField(
        blank=True, null=True, verbose_name='comment'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='updated at'
    )

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.comment) if len(str(self.comment)) <= 10 else str(self.comment)[:10] + " ..."


class CommentReply(models.Model):
    post_comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='comment_replays', verbose_name='post comment',
        null = True, blank = True
    )
    replied_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,
        related_name='comment_replays', verbose_name='replied by',
        null=True, blank=True
    )
    reply = models.TextField(
        blank=True, null=True, verbose_name='reply'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='updated at'
    )

    class Meta:
        ordering = ['-updated_at']


    def __str__(self):
        return str(self.reply) if len(str(self.reply)) <= 10 else str(self.reply)[:10] + " ..."