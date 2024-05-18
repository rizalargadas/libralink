from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import BookForm
from .models import Book
from transaction.models import Transaction


@login_required
def list_books(request):
    """ Display a list of books, optionally filtered by a search query. """
    query = request.GET.get('q', '').replace('-', ' ')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query) |
            Q(isbn__icontains=query)
        )
        if not books.exists():
            messages.error(request, "No books found!")
    else:
        books = Book.objects.all()

    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'book/list_books.html', {'books': books, 'page_obj': page_obj})


@login_required
def book_detail(request, pk):
    """ Display the details of a single book, along with its related transactions. """
    book = Book.objects.get(pk=pk)
    transactions = Transaction.objects.filter(book=book)
    return render(request, 'book/book_detail.html', {'book': book, 'transactions': transactions})


@login_required
def add_book(request):
    """ Add a new book to the database. """
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book:list_books')
        else:
            messages.error(request, 'Invalid Input.')
            return render(request, 'book/add_book.html')
    else:
        form = BookForm()
        return render(request, 'book/add_book.html', {'form': form})


@login_required
def edit_book(request, pk):
    """ Edit the details of an existing book. """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book was successfully updated!")
            return redirect(reverse('book:book_detail', args=[pk]))
        else:
            messages.error(
                request, "Invalid input.")
    else:
        form = BookForm(instance=book)
    return render(request, 'book/edit_book.html', {'form': form, 'book': book})


# def delete_book(request, pk):
#     """ Delete a book from the database. """
#     book = Book.objects.get(pk=pk)
#     book.delete()
#     messages.success(request, "Book was successfully deleted!")
#     return redirect('book:list_books')
