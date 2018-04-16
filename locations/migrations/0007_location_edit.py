# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_location_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='edit',
            field=models.BooleanField(default=False),
        ),
    ]
