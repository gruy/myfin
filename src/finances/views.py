from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.views.generic import CreateView, ListView, TemplateView
from django.urls import reverse_lazy

from src.mixins import BS4Form, BS4ModelForm

from .forms import TransactionForm
from .models import Category, Transaction


class IndexView(LoginRequiredMixin, CreateView):
    form_class = TransactionForm
    success_url = reverse_lazy('index')
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        self.transactions = Transaction.objects.all()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['transactions'] = self.transactions
        ctx['by_months'] = list(self.transactions.annotate(month=TruncMonth('date')).values('month').annotate(amount=Sum('amount')).order_by())
        ctx['by_months'].reverse()
        ctx['sum'] = self.transactions.aggregate(sum=Sum('amount'))['sum']
        return ctx

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        return super().form_valid(form)


class MonthView(LoginRequiredMixin, ListView):
    context_object_name = 'transactions'
    model = Transaction
    template_name = 'month.html'

    def get(self, request, *args, **kwargs):
        self.month = kwargs['month']
        self.year = kwargs['year']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['month'] = self.month
        ctx['year'] = self.year
        ctx['sum'] = self.object_list.aggregate(sum=Sum('amount'))['sum']
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(date__year=self.year, date__month=self.month)
