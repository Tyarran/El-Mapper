# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapper', '0003_auto_20151016_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_fk', models.CharField(max_length=250)),
                ('internal_fk', models.ForeignKey(to='mapper.Brand')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CategoryConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_fk', models.CharField(max_length=250)),
                ('internal_fk', models.ForeignKey(to='mapper.Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ColorConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_fk', models.CharField(max_length=250)),
                ('internal_fk', models.ForeignKey(to='mapper.Color')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FieldMappingConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_field_name', models.CharField(max_length=250)),
                ('product_field', models.CharField(max_length=250, choices=[('id', 'id'), (b'name', b'name'), (b'description', b'description'), (b'price', b'price'), (b'brand', b'brand'), (b'category', b'category'), (b'color', b'color')])),
                ('color', models.ForeignKey(to='mapper.Color')),
            ],
        ),
    ]
