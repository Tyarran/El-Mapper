# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapper', '0005_auto_20151020_2115'),
    ]

    operations = [
        migrations.CreateModel(
            name='MappingResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('result', models.TextField()),
                ('config', models.ForeignKey(to='mapper.MappingConfig')),
            ],
        ),
        migrations.RemoveField(
            model_name='importedproductcsv',
            name='mapping_config',
        ),
        migrations.AddField(
            model_name='mappingresult',
            name='csv',
            field=models.ForeignKey(to='mapper.ImportedProductCSV'),
        ),
    ]
