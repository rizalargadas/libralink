from datetime import timedelta
from django.db import transaction as db_transaction
from transaction.models import Transaction
from patron.models import Patron
from book.models import Book


def checkout_book(patron_id, book_id, date_borrowed, date_due=None):
    try:
        patron = Patron.objects.get(id=patron_id, account_status='active')
        book = Book.objects.get(id=book_id, available_copies__gt=0)

        with db_transaction.atomic():
            # Create the transaction
            new_transaction = Transaction(
                patron=patron,
                book=book,
                date_borrowed=date_borrowed,
                date_due=date_due or (date_borrowed + timedelta(days=7))
            )
            new_transaction.save()

            # Update book inventory
            book.available_copies -= 1
            book.copies_on_loan += 1
            book.save()

            # Update patron's pending returns
            patron.pending_return += 1
            patron.save()

            return new_transaction
    except (Patron.DoesNotExist, Book.DoesNotExist):
        return None


transaction_id = 3


def check_patron_status(num_of_late_returns):
    if num_of_late_returns > 3:
        status = 'red'
    elif num_of_late_returns > 0:
        status = 'yellow'
    else:
        status = 'green'

    return status


def update_book_and_patron_on_return(transaction, returned_date):
    transaction.is_returned = True
    transaction.date_returned = returned_date
    transaction.save()

    book = transaction.book
    patron = transaction.patron
    book.available_copies += 1
    book.copies_on_loan -= 1
    book.save()

    allowable_loan_days = transaction.date_due - transaction.date_borrowed
    actual_loaned_days = returned_date - transaction.date_borrowed
    if actual_loaned_days > allowable_loan_days:
        patron.late_returns += 1
        patron.status = check_patron_status(patron.late_returns)

    patron.pending_return -= 1
    patron.save()
