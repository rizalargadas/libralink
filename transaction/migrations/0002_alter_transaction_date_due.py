# Generated by Django 5.0.6 on 2024-05-08 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date_due',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
