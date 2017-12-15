# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-15 15:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_homepagerelatedlink_standardpagerelatedlink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepagerelatedlink',
            name='link_document',
        ),
        migrations.RemoveField(
            model_name='homepagerelatedlink',
            name='link_page',
        ),
        migrations.RemoveField(
            model_name='homepagerelatedlink',
            name='page',
        ),
        migrations.RemoveField(
            model_name='standardpagerelatedlink',
            name='link_document',
        ),
        migrations.RemoveField(
            model_name='standardpagerelatedlink',
            name='link_page',
        ),
        migrations.RemoveField(
            model_name='standardpagerelatedlink',
            name='page',
        ),
        migrations.DeleteModel(
            name='HomePageRelatedLink',
        ),
        migrations.DeleteModel(
            name='StandardPageRelatedLink',
        ),
    ]