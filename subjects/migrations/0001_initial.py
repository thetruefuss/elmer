# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
                ('board', models.ForeignKey(related_name='submitted_subjects', to='boards.Board')),
                ('mentioned', models.ManyToManyField(blank=True, related_name='m_in_subjects', to=settings.AUTH_USER_MODEL)),
                ('points', models.ManyToManyField(blank=True, related_name='liked_subjects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
