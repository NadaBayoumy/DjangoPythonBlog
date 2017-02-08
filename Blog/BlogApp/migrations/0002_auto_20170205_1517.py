# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-05 15:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForbiddenWords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forbiddenWord', models.CharField(max_length=180)),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='users',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]