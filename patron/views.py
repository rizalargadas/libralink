from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Patron
from .forms import PatronForm
from transaction.models import Transaction


@login_required
def patron_list(request):
    query = request.GET.get('q', '')
    if query:
        patrons = Patron.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(membership_id__icontains=query) |
            Q(status__icontains=query) |
            Q(account_status__icontains=query)
        )
        if not patrons.exists():
            messages.error(
                request, 'No patrons found matching the search criteria.')
    else:
        patrons = Patron.objects.all()

    paginator = Paginator(patrons, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'patron/patron_list.html', {'patrons': patrons, 'page_obj': page_obj})


@login_required
def add_patron(request):
    if request.method == 'POST':
        form = PatronForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Patron was successfully added.')
            return redirect('patron:patron_list')
        else:
            messages.error(
                request, 'Invalid input. Please check the errors below.')
    else:
        form = PatronForm()

    return render(request, 'patron/add_patron.html', {'form': form})


@login_required
def patron_detail(request, pk):
    patron = get_object_or_404(Patron, pk=pk)
    transactions = Transaction.objects.filter(patron=patron)
    paginator = Paginator(transactions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'patron/patron_detail.html', {'patron': patron, 'transactions': transactions, 'page_obj': page_obj})


@login_required
def edit_patron(request, pk):
    patron = get_object_or_404(Patron, pk=pk)
    if request.method == 'POST':
        form = PatronForm(request.POST, instance=patron)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patron was edited successfully.')
            return redirect(reverse('patron:patron_detail', args=[pk]))
        else:
            messages.error(
                request, 'Invalid input. Please check the errors below.')
    else:
        form = PatronForm(instance=patron)

    return render(request, 'patron/edit_patron.html', {'form': form, 'patron': patron_detail})


@login_required
def deactivate_patron(request, pk):
    patron = get_object_or_404(Patron, pk=pk)
    patron.account_status = 'deactivated'
    patron.status = 'red'
    patron.save()
    messages.info(request, 'Patron account has been deactivated.')
    return redirect(reverse('patron:patron_detail', args=[pk]))
