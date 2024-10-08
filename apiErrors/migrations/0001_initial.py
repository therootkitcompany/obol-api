# Generated by Django 5.0.9 on 2024-09-19 15:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiErrorLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('error_message', models.TextField()),
                ('error_traceback', models.TextField(blank=True, null=True)),
                ('url', models.URLField()),
                ('method', models.CharField(max_length=10)),
                ('status_code', models.IntegerField()),
                ('request_data', models.TextField(blank=True, null=True)),
                ('query_params', models.TextField(blank=True, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('referer', models.URLField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
