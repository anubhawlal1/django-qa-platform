# Generated by Django 5.0.2 on 2025-04-08 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
