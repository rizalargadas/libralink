from django.db import models
import uuid


class Patron(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    membership_id = models.CharField(max_length=50, unique=True)
    late_returns = models.PositiveIntegerField(default=0)
    pending_return = models.PositiveIntegerField(default=0)
    PATRON_STATUS_CHOICES = [
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
    ]

    status = models.CharField(
        max_length=100, choices=PATRON_STATUS_CHOICES, default='green')

    ACCOUNT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('deactivated', 'Deactivated')
    ]

    account_status = models.CharField(
        max_length=100, choices=ACCOUNT_STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
