from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from book.models import Book
from patron.models import Patron
from transaction.models import Transaction


@login_required
def dashboard(request):
    """ Display the dashboard page for logged-in users. """
    books = Book.objects.all()
    patrons = Patron.objects.all()
    transactions = Transaction.objects.all()
    return render(request, 'core/dashboard.html', {'books': books, 'patrons': patrons, 'transactions': transactions})


def register(request):
    """ Handle user registration. """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect(reverse('core:dashboard'))
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below.")

    else:
        form = CustomUserCreationForm()

    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            librarian_id = form.cleaned_data.get('librarian_id')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,
                                password=password, librarian_id=librarian_id)
            if user is not None:
                login(request, user)
                messages.info(
                    request, f"You are now successfully logged in as {username}.")
                return redirect('core:dashboard')
            else:
                messages.error(request, "Invalid Credentials.")
        else:
            messages.error(request, "Invalid Credentials.")

    else:
        form = CustomAuthenticationForm()

    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    """ Handle user logout. """
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('core:login')
