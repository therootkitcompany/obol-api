# Generated by Django 5.0.9 on 2024-09-24 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0005_alter_donation_stripesessionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='clientIp',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
