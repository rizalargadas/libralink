# Generated by Django 5.0.6 on 2024-05-09 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_rename_pending_returns_book_copies_on_loan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='copies_on_loan',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
