# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulp_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={},
        ),
        migrations.AlterModelOptions(
            name='repository',
            options={},
        ),
        migrations.AlterModelTable(
            name='content',
            table='pulp_app_content',
        ),
        migrations.AlterModelTable(
            name='repository',
            table='pulp_app_repository',
        ),
        migrations.AlterModelTable(
            name='repositorycontent',
            table='pulp_app_repositorycontent',
        ),
    ]
