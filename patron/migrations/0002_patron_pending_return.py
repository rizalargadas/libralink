# Generated by Django 5.0.6 on 2024-05-08 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patron',
            name='pending_return',
            field=models.IntegerField(blank=True, default=0, editable=False, null=True),
        ),
    ]
