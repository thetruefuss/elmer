# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('dp', models.ImageField(blank=True, null=True, upload_to='dps/')),
                ('dob', models.DateField(blank=True, null=True)),
                ('member_since', models.DateTimeField(default=django.utils.timezone.now)),
                ('contact_list', models.ManyToManyField(blank=True, related_name='contacters', to=settings.AUTH_USER_MODEL)),
                ('followers', models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('pending_list', models.ManyToManyField(blank=True, related_name='my_pending_requests', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-member_since',),
            },
        ),
    ]
