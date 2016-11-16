# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pulp.app.models.storage
import uuid
import pulp.app.fields
import django.core.validators
import pulp.app.models.auth


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('username', models.CharField(verbose_name='username', max_length=150, unique=True, error_messages={'unique': 'A user with that username already exists.'}, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')])),
                ('groups', models.ManyToManyField(verbose_name='groups', to='auth.Group', blank=True, related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', to='auth.Permission', blank=True, related_name='user_set', help_text='Specific permissions for this user.', related_query_name='user')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', pulp.app.models.auth.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('file', models.FileField(max_length=255, db_index=True, upload_to=pulp.app.models.storage.StoragePath())),
                ('downloaded', models.BooleanField(default=False, db_index=True)),
                ('requested', models.BooleanField(default=False, db_index=True)),
                ('relative_path', models.TextField(db_index=True, default=None)),
                ('size', models.IntegerField(null=True, blank=True)),
                ('md5', models.CharField(null=True, max_length=32, blank=True)),
                ('sha1', models.CharField(null=True, max_length=40, blank=True)),
                ('sha224', models.CharField(null=True, max_length=56, blank=True)),
                ('sha256', models.CharField(null=True, max_length=64, blank=True)),
                ('sha384', models.CharField(null=True, max_length=96, blank=True)),
                ('sha512', models.CharField(null=True, max_length=128, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('object_id', models.UUIDField()),
                ('key', models.TextField()),
                ('value', models.TextField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('name', models.TextField(unique=True, db_index=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('type', models.TextField(default=None)),
            ],
            options={
                'verbose_name_plural': 'content',
            },
        ),
        migrations.CreateModel(
            name='DownloadCatalog',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('url', models.TextField(blank=True, validators=[django.core.validators.URLValidator])),
                ('artifact', models.ForeignKey(to='pulp_app.Artifact')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Importer',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('type', models.TextField(default=None)),
                ('name', models.TextField(db_index=True)),
                ('last_updated', models.DateTimeField(null=True, auto_now=True)),
                ('feed_url', models.TextField()),
                ('validate', models.BooleanField(default=True)),
                ('ssl_ca_certificate', models.TextField(blank=True)),
                ('ssl_client_certificate', models.TextField(blank=True)),
                ('ssl_client_key', models.TextField(blank=True)),
                ('ssl_validation', models.BooleanField(default=True)),
                ('proxy_url', models.TextField(blank=True)),
                ('basic_auth_user', models.TextField(blank=True)),
                ('basic_auth_password', models.TextField(blank=True)),
                ('max_download_bandwidth', models.IntegerField(null=True)),
                ('max_concurrent_downloads', models.IntegerField(null=True)),
                ('download_policy', models.TextField(choices=[('immediate', 'Download Immediately'), ('on_demand', 'Download On Demand'), ('background', 'Download In Background')])),
                ('last_sync', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'default_related_name': 'importers',
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('object_id', models.UUIDField()),
                ('key', models.TextField()),
                ('value', models.TextField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProgressReport',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('message', models.TextField()),
                ('state', models.TextField(choices=[('waiting', 'Waiting'), ('skipped', 'Skipped'), ('running', 'Running'), ('completed', 'Completed'), ('failed', 'Failed'), ('canceled', 'Canceled')], default='waiting')),
                ('total', models.IntegerField(null=True)),
                ('done', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('type', models.TextField(default=None)),
                ('name', models.TextField(db_index=True)),
                ('last_updated', models.DateTimeField(null=True, auto_now=True)),
                ('auto_publish', models.BooleanField(default=True)),
                ('relative_path', models.TextField(blank=True)),
                ('last_published', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'default_related_name': 'publishers',
            },
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('name', models.TextField(unique=True, db_index=True)),
                ('description', models.TextField(blank=True)),
                ('last_content_added', models.DateTimeField(null=True, blank=True)),
                ('last_content_removed', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'repositories',
            },
        ),
        migrations.CreateModel(
            name='RepositoryContent',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('content', models.ForeignKey(to='pulp_app.Content')),
                ('repository', models.ForeignKey(to='pulp_app.Repository')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RepositoryGroup',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('name', models.TextField(unique=True, db_index=True)),
                ('description', models.TextField(blank=True)),
                ('members', models.ManyToManyField(to='pulp_app.Repository')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReservedResource',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('resource', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Scratchpad',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('object_id', models.UUIDField()),
                ('key', models.TextField()),
                ('value', models.TextField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('group', models.UUIDField(null=True)),
                ('state', models.TextField(choices=[('waiting', 'Waiting'), ('skipped', 'Skipped'), ('running', 'Running'), ('completed', 'Completed'), ('failed', 'Failed'), ('canceled', 'Canceled')])),
                ('started_at', models.DateTimeField(null=True)),
                ('finished_at', models.DateTimeField(null=True)),
                ('non_fatal_errors', pulp.app.fields.JSONField()),
                ('result', pulp.app.fields.JSONField(default=[])),
                ('parent', models.ForeignKey(to='pulp_app.Task', related_name='spawned_tasks', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskLock',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('name', models.TextField(unique=True, db_index=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('lock', models.TextField(choices=[('CeleryBeat', 'Celery Beat Lock'), ('ResourceManager', 'Resource Manager Lock')], unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskTag',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('name', models.TextField()),
                ('task', models.ForeignKey(to='pulp_app.Task', related_name='tags', related_query_name='tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('name', models.TextField(unique=True, db_index=True)),
                ('last_heartbeat', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='task',
            name='worker',
            field=models.ForeignKey(to='pulp_app.Worker', related_name='tasks', null=True),
        ),
        migrations.AddField(
            model_name='reservedresource',
            name='task',
            field=models.OneToOneField(to='pulp_app.Task'),
        ),
        migrations.AddField(
            model_name='reservedresource',
            name='worker',
            field=models.ForeignKey(related_name='reservations', to='pulp_app.Worker'),
        ),
        migrations.AddField(
            model_name='repository',
            name='content',
            field=models.ManyToManyField(related_name='repositories', to='pulp_app.Content', through='pulp_app.RepositoryContent'),
        ),
        migrations.AddField(
            model_name='publisher',
            name='repository',
            field=models.ForeignKey(to='pulp_app.Repository'),
        ),
        migrations.AddField(
            model_name='progressreport',
            name='task',
            field=models.ForeignKey(to='pulp_app.Task'),
        ),
        migrations.AddField(
            model_name='importer',
            name='repository',
            field=models.ForeignKey(to='pulp_app.Repository'),
        ),
        migrations.AddField(
            model_name='downloadcatalog',
            name='importer',
            field=models.ForeignKey(to='pulp_app.Importer'),
        ),
        migrations.AddField(
            model_name='consumer',
            name='publishers',
            field=models.ManyToManyField(related_name='consumers', to='pulp_app.Publisher'),
        ),
        migrations.AddField(
            model_name='artifact',
            name='content',
            field=models.ForeignKey(related_name='artifacts', to='pulp_app.Content'),
        ),
        migrations.CreateModel(
            name='ProgressBar',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('pulp_app.progressreport',),
        ),
        migrations.CreateModel(
            name='ProgressSpinner',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('pulp_app.progressreport',),
        ),
        migrations.AlterUniqueTogether(
            name='scratchpad',
            unique_together=set([('key', 'content_type', 'object_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='publisher',
            unique_together=set([('repository', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='notes',
            unique_together=set([('key', 'content_type', 'object_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='importer',
            unique_together=set([('repository', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='artifact',
            unique_together=set([('content', 'relative_path')]),
        ),
    ]
