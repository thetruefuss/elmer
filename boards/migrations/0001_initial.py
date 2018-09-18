# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='title')),
                ('description', models.TextField(max_length=500)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='board_covers/')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('admins', models.ManyToManyField(related_name='inspected_boards', to=settings.AUTH_USER_MODEL)),
                ('banned_users', models.ManyToManyField(related_name='forbidden_boards', to=settings.AUTH_USER_MODEL)),
                ('subscribers', models.ManyToManyField(related_name='subscribed_boards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
