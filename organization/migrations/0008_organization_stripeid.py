# Generated by Django 5.0.6 on 2024-09-13 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_organization_web'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='stripeId',
            field=models.CharField(default='', max_length=100),
        ),
    ]
