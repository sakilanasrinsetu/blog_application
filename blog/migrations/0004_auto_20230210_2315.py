# Generated by Django 3.2.6 on 2023-02-10 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_alter_post_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commented_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='commentreply',
            name='post_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_replays', to='blog.comment', verbose_name='post comment'),
        ),
    ]