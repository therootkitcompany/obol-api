# Generated by Django 5.0.6 on 2024-05-21 13:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0006_rename_creditcard_donation_credittoken_and_more'),
        ('organization', '0005_remove_organization_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='organization',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='donations', related_query_name='donation', to='organization.organization'),
            preserve_default=False,
        ),
    ]
