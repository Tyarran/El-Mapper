# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapper', '0004_brandconfig_categoryconfig_colorconfig_fieldmappingconfig'),
    ]

    operations = [
        migrations.CreateModel(
            name='MappingConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('json', models.TextField(null=True, blank=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='brandconfig',
            name='internal',
        ),
        migrations.RemoveField(
            model_name='categoryconfig',
            name='internal',
        ),
        migrations.RemoveField(
            model_name='colorconfig',
            name='internal',
        ),
        migrations.DeleteModel(
            name='FieldMappingConfig',
        ),
        migrations.DeleteModel(
            name='BrandConfig',
        ),
        migrations.DeleteModel(
            name='CategoryConfig',
        ),
        migrations.DeleteModel(
            name='ColorConfig',
        ),
        migrations.AddField(
            model_name='importedproductcsv',
            name='mapping_config',
            field=models.ForeignKey(blank=True, to='mapper.MappingConfig', null=True),
        ),
    ]
