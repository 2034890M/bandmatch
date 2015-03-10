# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('content', models.TextField()),
                ('date', models.DateField()),
                ('looking_for', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('demo', models.FileField(upload_to=b'band_demos', blank=True)),
                ('location', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to=b'band_images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('content', models.TextField()),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_info', models.TextField()),
                ('description', models.TextField()),
                ('privacy', models.IntegerField(default=1)),
                ('demo', models.FileField(upload_to=b'player_demos', blank=True)),
                ('instrument', models.CharField(default=b'None', max_length=128)),
                ('location', models.CharField(default=b'Nowhere', max_length=256)),
                ('image', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='recipients',
            field=models.ManyToManyField(to='bandmatch.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(related_name=b'sender', to='bandmatch.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='band',
            name='members',
            field=models.ManyToManyField(to='bandmatch.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advert',
            name='band',
            field=models.ForeignKey(to='bandmatch.Band'),
            preserve_default=True,
        ),
    ]
