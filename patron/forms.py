from django import forms
from .models import Patron


class PatronForm(forms.ModelForm):
    class Meta:
        model = Patron
        fields = ['name', 'email', 'membership_id', 'status', 'account_status']
