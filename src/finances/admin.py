from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import *


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'amount', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
