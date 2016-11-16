# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulp_app', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestContent',
            fields=[
                ('content_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='pulp_app.Content')),
                ('name', models.TextField()),
            ],
            bases=('pulp_app.content',),
        ),
        migrations.CreateModel(
            name='TestImporter',
            fields=[
                ('importer_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='pulp_app.Importer')),
                ('test_field', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('pulp_app.importer',),
        ),
        migrations.CreateModel(
            name='TestPublisher',
            fields=[
                ('publisher_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='pulp_app.Publisher')),
                ('test_field', models.TextField()),
            ],
            bases=('pulp_app.publisher',),
        ),
    ]
