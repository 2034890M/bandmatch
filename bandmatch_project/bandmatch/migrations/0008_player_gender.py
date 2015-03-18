# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandmatch', '0007_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='gender',
            field=models.CharField(default=b'unknown', max_length=25, choices=[(b'unknown', b'do not wish to specify'), (b'm', b'male'), (b'f', b'female')]),
            preserve_default=True,
        ),
    ]
