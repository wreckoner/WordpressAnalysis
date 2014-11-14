# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wordpress',
            fields=[
                ('url', models.CharField(max_length=175, unique=True, serialize=False, primary_key=True)),
                ('level', models.CharField(max_length=10)),
                ('published', models.DateTimeField()),
                ('parent', models.CharField(max_length=150, null=True)),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(max_length=100, blank=True)),
                ('content', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
