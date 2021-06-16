from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import Http404
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


class MonthRootView(LoginRequiredMixin, TemplateView):
    template_name = 'month_root.html'

    def get(self, request, *args, **kwargs):
        self.month = kwargs['month']
        self.year = kwargs['year']
        self.category = None
        self.breadcrumbs = []
        category_id = kwargs.get('category_id', None)

        if category_id:
            try:
                self.category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                raise Http404
            categories = list(self.category.get_descendants())
            categories.append(self.category)
            self.transactions = Transaction.objects.filter(category__in=categories, date__year=self.year, date__month=self.month)
            self.category.amount = Transaction.objects.filter(category=self.category, date__year=self.year, date__month=self.month).aggregate(sum=Sum('amount'))['sum']
            roots = self.category.get_children()
            self.breadcrumbs.append(self.category)
            _parent = self.category.get_parent()
            while _parent:
                self.breadcrumbs.append(_parent)
                _parent = _parent.get_parent()
            self.breadcrumbs.reverse()
        else:
            self.transactions = Transaction.objects.filter(date__year=self.year, date__month=self.month)
            roots = Category.get_root_nodes()

        self.result = []
        for root in roots:
            categories = list(root.get_descendants())
            categories.append(root)
            amount = self.transactions.filter(category__in=categories).aggregate(sum=Sum('amount'))['sum']
            if amount:
                self.result.append({
                    'category': root,
                    'amount': amount,
                })

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['month'] = self.month
        ctx['year'] = self.year
        ctx['sum'] = self.transactions.aggregate(sum=Sum('amount'))['sum']
        ctx['result'] = self.result
        ctx['category'] = self.category
        ctx['breadcrumbs'] = self.breadcrumbs
        return ctx


class MonthDetailView(LoginRequiredMixin, ListView):
    context_object_name = 'transactions'
    model = Transaction
    template_name = 'month_detail.html'

    def get(self, request, *args, **kwargs):
        self.month = kwargs['month']
        self.year = kwargs['year']
        self.category = None
        category_id = kwargs.get('category_id', None)
        self.breadcrumbs = []
        if category_id:
            try:
                self.category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                raise Http404
            self.breadcrumbs.append(self.category)
            _parent = self.category.get_parent()
            while _parent:
                self.breadcrumbs.append(_parent)
                _parent = _parent.get_parent()
            self.breadcrumbs.reverse()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['month'] = self.month
        ctx['year'] = self.year
        ctx['sum'] = self.object_list.aggregate(sum=Sum('amount'))['sum']
        ctx['category'] = self.category
        ctx['breadcrumbs'] = self.breadcrumbs
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        if self.category:
            qs = qs.filter(category=self.category, date__year=self.year, date__month=self.month)
        else:
            qs = qs.filter(date__year=self.year, date__month=self.month)
        return qs
