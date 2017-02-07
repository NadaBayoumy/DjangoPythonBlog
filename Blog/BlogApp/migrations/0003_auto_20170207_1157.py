# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 11:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0002_auto_20170205_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='postPic',
            field=models.ImageField(upload_to='static/img', verbose_name='Post Image'),
        ),
        migrations.AlterField(
            model_name='post',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reply',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BlogApp.Reply'),
        ),
    ]
