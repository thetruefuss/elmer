# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=500, unique=True, db_index=True)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='title')),
                ('description', models.TextField(max_length=2000)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='covers/')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('admins', models.ManyToManyField(related_name='inspected_boards', to=settings.AUTH_USER_MODEL)),
                ('banned_users', models.ManyToManyField(related_name='forbidden_boards', to=settings.AUTH_USER_MODEL)),
                ('subscribers', models.ManyToManyField(related_name='subscribed_boards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Board',
                'verbose_name_plural': 'Boards',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('body', models.TextField(max_length=2000)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('commenter', models.ForeignKey(related_name='posted_comments', to=settings.AUTH_USER_MODEL)),
                ('reply', models.ForeignKey(blank=True, null=True, related_name='comment_reply', to='frontboard.Comment')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='FeaturedPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=120)),
                ('photo', models.ImageField(upload_to='FeaturedPostPhotos/')),
                ('link', models.URLField(max_length=2000, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Featured Post',
                'verbose_name_plural': 'Featured Posts',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('board', models.ForeignKey(blank=True, null=True, related_name='board_reports', to='frontboard.Board')),
                ('comment', models.ForeignKey(blank=True, null=True, related_name='comment_reports', to='frontboard.Comment')),
                ('reporter', models.ForeignKey(null=True, related_name='reported', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=150, db_index=True)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='title')),
                ('body', models.TextField(max_length=5000, blank=True, null=True)),
                ('photo', models.ImageField(verbose_name='Add image (optional)', blank=True, null=True, upload_to='subject_photos/')),
                ('rank_score', models.FloatField(default=0.0)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(related_name='posted_subjects', to=settings.AUTH_USER_MODEL)),
                ('board', models.ForeignKey(related_name='submitted_subjects', to='frontboard.Board')),
                ('mentioned', models.ManyToManyField(blank=True, related_name='m_in_subjects', to=settings.AUTH_USER_MODEL)),
                ('points', models.ManyToManyField(blank=True, related_name='liked_subjects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='report',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, related_name='subject_reports', to='frontboard.Subject'),
        ),
        migrations.AddField(
            model_name='comment',
            name='subject',
            field=models.ForeignKey(related_name='comments', to='frontboard.Subject'),
        ),
    ]
