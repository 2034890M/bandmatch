# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bandmatch.models


class Migration(migrations.Migration):

    dependencies = [
        ('bandmatch', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='instrument',
        ),
        migrations.AddField(
            model_name='player',
            name='instruments',
            field=bandmatch.models.ListField(default=[]),
            preserve_default=False,
        ),
    ]
