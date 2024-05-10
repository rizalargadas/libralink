from django.db import models
import uuid


class Book(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    book_cover = models.ImageField(
        upload_to='book_covers/',
        default='default_images/default_book_cover.png',
        blank=True, null=True
    )
    description = models.TextField(null=True, blank=True)
    isbn = models.CharField(max_length=200, unique=True)
    publisher = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    available_copies = models.IntegerField()
    copies_on_loan = models.PositiveIntegerField(
        null=True, blank=True, default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
