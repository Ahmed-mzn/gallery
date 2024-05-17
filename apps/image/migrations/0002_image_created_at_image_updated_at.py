# Generated by Django 5.0.6 on 2024-05-16 23:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]