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
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25, null=True, blank=True)),
                ('avatar', models.ImageField(null=True, upload_to=b'avatars/%Y/%m/%d/', blank=True)),
                ('description', models.TextField(default=None, max_length=500, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
