# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandmatch', '0008_player_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='privacy',
            field=models.IntegerField(default=1, choices=[(b'1', b'on'), (b'0', b'off')]),
            preserve_default=True,
        ),
    ]
