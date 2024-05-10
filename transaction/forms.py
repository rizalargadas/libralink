from django import forms
from django.forms import DateTimeInput
from .models import Patron, Book, Transaction
from django.forms import ModelChoiceField
from django.utils import timezone
from datetime import datetime


class CheckoutForm(forms.Form):
    patron = ModelChoiceField(
        queryset=Patron.objects.filter(account_status='active'))
    date_borrowed = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    date_due = forms.DateTimeField(required=False, widget=DateTimeInput(
        attrs={'type': 'datetime-local'}))

    def clean(self):
        cleaned_data = super().clean()
        # Add custom validation if needed
        return cleaned_data


class ReturnForm(forms.Form):
    book = ModelChoiceField(queryset=Book.objects.all())
    patron = ModelChoiceField(
        queryset=Patron.objects.filter(account_status='active'))

    def __init__(self, *args, **kwargs):
        book_id = kwargs.pop('book_id', None)
        super().__init__(*args, **kwargs)
        # Update the queryset if needed, can also filter based on some logic
        self.fields['book'].queryset = Book.objects.all()
        if book_id:
            # Set the initial value for the book field
            self.fields['book'].initial = Book.objects.filter(
                id=book_id).first()

    def clean(self):
        cleaned_data = super().clean()
        # Add custom validation if needed
        return cleaned_data


class ExistingTransactionsForm(forms.Form):
    transactions = ModelChoiceField(queryset=Transaction.objects.all())
    date_returned = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=datetime.now()
    )

    def __init__(self, *args, **kwargs):
        book_id = kwargs.pop('book_id', None)
        patron_id = kwargs.pop('patron_id', None)
        super().__init__(*args, **kwargs)

        if book_id and patron_id:
            self.fields['transactions'].queryset = Transaction.objects.filter(
                book=book_id, patron=patron_id, is_returned=False)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
