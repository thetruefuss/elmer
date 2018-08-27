# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontboard', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FeaturedPost',
        ),
        migrations.AlterModelOptions(
            name='board',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created',)},
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ('-created',)},
        ),
    ]
