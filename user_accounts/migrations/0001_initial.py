# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frontboard', '0001_initial'),
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
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
                'ordering': ('-member_since',),
            },
        ),
        migrations.CreateModel(
            name='subject_notify',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('notif_type', models.CharField(max_length=500, default='Comment on Subject', choices=[('subject_mentioned', 'Mentioned in Subject'), ('comment_mentioned', 'Mentioned in Comment'), ('comment', 'Comment on Subject'), ('follow', 'Followed by someone'), ('sent_msg_request', 'Sent a Message Request'), ('confirmed_msg_request', 'Sent a Message Request')])),
                ('is_read', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('Actor', models.ForeignKey(related_name='c_acts', to=settings.AUTH_USER_MODEL)),
                ('Object', models.ForeignKey(blank=True, null=True, related_name='act_notif', to='frontboard.Subject')),
                ('Target', models.ForeignKey(related_name='c_notif', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ('-created',),
            },
        ),
    ]
