# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djbetty.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideohubVideo',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=512)),
                ('description', models.TextField(default=b'', blank=True)),
                ('keywords', models.TextField(default=b'', blank=True)),
                ('image', djbetty.fields.ImageField(default=None, alt_field=b'_image_alt', null=True, caption_field=b'_image_caption', blank=True)),
                ('_image_alt', models.CharField(max_length=255, null=True, editable=False, blank=True)),
                ('_image_caption', models.CharField(max_length=255, null=True, editable=False, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
