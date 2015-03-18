# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandmatch', '0005_auto_20150317_1234'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('advert', models.ForeignKey(to='bandmatch.Advert')),
                ('replier', models.ForeignKey(to='bandmatch.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
