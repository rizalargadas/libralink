# Generated by Django 5.0.6 on 2024-05-09 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0007_alter_patron_late_returns'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patron',
            name='pending_return',
            field=models.PositiveIntegerField(default=0),
        ),
    ]