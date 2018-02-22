# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-26 20:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log_reg', '0003_author_book_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='author',
            name='last_name',
        ),
    ]
