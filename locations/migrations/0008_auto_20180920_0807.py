# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0007_location_edit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ['position']},
        ),
    ]
