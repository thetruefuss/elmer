# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0001_initial'),
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('board', models.ForeignKey(blank=True, null=True, related_name='board_reports', to='boards.Board')),
                ('comment', models.ForeignKey(blank=True, null=True, related_name='comment_reports', to='comments.Comment')),
                ('reporter', models.ForeignKey(null=True, related_name='reported', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(blank=True, null=True, related_name='subject_reports', to='subjects.Subject')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
