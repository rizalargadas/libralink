from django.db import models
from datetime import timedelta

from patron.models import Patron
from book.models import Book
import uuid


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patron = models.ForeignKey(
        Patron, related_name='transactions', on_delete=models.PROTECT)
    book = models.ForeignKey(
        Book, related_name='transactions', on_delete=models.PROTECT)
    date_borrowed = models.DateTimeField()
    date_due = models.DateTimeField(null=True, blank=True)
    date_returned = models.DateTimeField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_borrowed']

    def save(self, *args, **kwargs):
        if not self.date_due:  # Set date_due only if it's not already set
            self.date_due = self.date_borrowed + timedelta(days=7)
        super().save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        formatted_date = self.date_borrowed.strftime('%m-%d-%Y')
        return f"{formatted_date} | {self.patron} | tn#{self.id}"
