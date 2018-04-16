# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_auto_20170706_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='position',
            field=models.IntegerField(default=0),
        ),
    ]
