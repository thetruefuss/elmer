# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog_Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=2000)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('body', models.TextField(max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('author', models.ForeignKey(related_name='post_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('photo', models.ImageField(upload_to='blog_photos/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=500)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='title')),
                ('body', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='blog_posts/')),
                ('status', models.CharField(max_length=10, default='draft', choices=[('draft', 'Draft'), ('published', 'Published')])),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ('-publish',),
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(related_name='comments', to='blog.Post'),
        ),
    ]
