# Generated by Django 5.0.6 on 2024-05-09 00:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_transaction_is_returned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]