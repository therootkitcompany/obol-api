# Generated by Django 5.0.9 on 2024-09-24 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0002_alter_donation_credittoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation',
            name='clientIp',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='creditToken',
        ),
        migrations.AddField(
            model_name='donation',
            name='stripeSessionId',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
    ]
