# Generated by Django 5.1.4 on 2025-01-23 12:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplementapp', '0003_registermodel_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='productmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='description',
            field=models.TextField(max_length=100),
        ),
    ]
