# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordpress', '0002_auto_20141114_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordpress',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
