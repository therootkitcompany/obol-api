# Generated by Django 5.0.6 on 2024-05-16 15:03

import encrypted_field.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_organization_bankaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='bankAccount',
            field=encrypted_field.fields.EncryptedField(max_length=50),
        ),
    ]
