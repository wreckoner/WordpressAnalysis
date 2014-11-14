# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordpress', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordpress',
            name='content',
            field=models.CharField(max_length=5000, blank=True),
        ),
    ]
