# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import precise_bbcode.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=100)),
                ('_text_rendered', models.TextField(null=True, editable=False, blank=True)),
                ('text', precise_bbcode.fields.BBCodeTextField(no_rendered_field=True)),
                ('sent', models.DateTimeField(auto_now_add=True)),
                ('replied', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['sent'],
            },
        ),
        migrations.CreateModel(
            name='MessageChain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('started', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='directmessage',
            name='chain',
            field=models.ForeignKey(to='directmessages.MessageChain'),
        ),
        migrations.AddField(
            model_name='directmessage',
            name='recipient',
            field=models.ForeignKey(related_name='received_direct_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='directmessage',
            name='sender',
            field=models.ForeignKey(related_name='sent_direct_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
