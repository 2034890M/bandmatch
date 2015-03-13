# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandmatch', '0003_auto_20150311_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='band',
            name='slug',
            field=models.SlugField(default='my_chemical_bromance', unique=True),
            preserve_default=False,
        ),
    ]
