from django import forms

from django_select2.forms import Select2Widget

from src.mixins import BS4ModelForm
from .models import Transaction


class TransactionForm(BS4ModelForm):
    class Meta:
        fields = ['date', 'category', 'quantity', 'unit', 'price', 'amount', 'comment', ]
        model = Transaction
        widgets = {
            'category': Select2Widget,
            'comment': forms.Textarea(attrs={'rows': 5}),
        }
