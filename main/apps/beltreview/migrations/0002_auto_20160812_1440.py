# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-12 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beltreview', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.TextField(default=1, max_length=2),
            preserve_default=False,
        ),
    ]
