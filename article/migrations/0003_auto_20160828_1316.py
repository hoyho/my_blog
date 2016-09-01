# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20160828_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='intro',
            field=models.TextField(null=True, max_length=500),
        ),
    ]
