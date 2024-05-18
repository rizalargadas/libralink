from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import CheckoutForm, ReturnForm, ExistingTransactionsForm
from .models import Transaction
from .services import checkout_book, update_book_and_patron_on_return
from book.models import Book
from patron.models import Patron


@login_required
def transaction_list(request):
    transactions = Transaction.objects.all()
    paginator = Paginator(transactions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'transaction/transaction_list.html', {'transactions': transactions, 'page_obj': page_obj})


@login_required
def transaction_checkout(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            patron = form.cleaned_data['patron']
            date_borrowed = form.cleaned_data['date_borrowed']
            date_due = form.cleaned_data.get('date_due')

            if checkout_book(patron.id, book.id, date_borrowed, date_due):
                messages.success(request, 'Checkout successful!')
                return redirect('book:list_books')

        messages.error(
            request, 'Checkout failed: Book not available or patron not active.')
    else:
        form = CheckoutForm(initial={'date_borrowed': datetime.now()})

    return render(request, 'transaction/checkout.html', {'form': form, 'book': book})


@login_required
def start_return_process(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    if request.method == 'POST':
        form = ReturnForm(request.POST, book_id=book.id)
        if form.is_valid():
            patron = form.cleaned_data['patron']
            existing_transactions_form = ExistingTransactionsForm(
                book_id=book.id, patron_id=patron.id)
            return render(request, 'transaction/dynamic_existing_transaction_by_patron.html',
                          {'transactions_form': existing_transactions_form, 'book': book})
        else:
            messages.error(
                request, 'No transaction history with this book and patron.')
    else:
        form = ReturnForm(book_id=book.id)

    return render(request, 'transaction/return.html', {'form': form, 'book': book})


@login_required
def return_success(request):
    if request.method != 'POST':
        return redirect('book:list_books')

    transaction_id = request.POST.get('transactions', '')
    date_returned = request.POST.get('date_returned', '')

    if not transaction_id or not date_returned:
        messages.error(request, 'Missing transaction ID or return date.')
        return redirect('book:list_books')

    try:
        transaction_date_returned = timezone.make_aware(datetime.strptime(
            date_returned, '%Y-%m-%dT%H:%M:%S'))

        transaction = get_object_or_404(Transaction, id=transaction_id)
        update_book_and_patron_on_return(
            transaction, transaction_date_returned)

        return render(request, 'transaction/return_successful.html')

    except Exception as e:
        messages.error(
            request, f"An error occurred during the transaction: {e}")
        return redirect('book:list_books')
