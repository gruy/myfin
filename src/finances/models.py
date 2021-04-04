from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from treebeard.mp_tree import MP_Node


TRANSACTION_INCOME = 1
TRANSACTION_EXPENSE = 2
TRANSACTION_TYPE = (
    (TRANSACTION_INCOME, _('Приход')),
    (TRANSACTION_EXPENSE, _('Расход')),
)

UNIT_KILOGRAM = 1
UNIT_PIECE = 2
UNIT_LITER = 3
UNIT_METER = 4
UNIT_PACK = 5
UNIT_CHOICES = (
    (UNIT_KILOGRAM, _('кг.')),
    (UNIT_PIECE, _('шт.')),
    (UNIT_LITER, _('л.')),
    (UNIT_METER, _('м.')),
    (UNIT_PACK, _('уп.')),
)

STATUS_NORMAL = 1
STATUS_DELETED = 2
STATUS_CHOICES = (
    (STATUS_NORMAL, _('Нормальный')),
    (STATUS_DELETED, _('Удалено')),
)


class Category(MP_Node):
    """
    Продукты: хлеб, молоко, мясо.
    Хозтовары: мыло, моющее для посуды, губки.
    Проезд: автобус, такси.
    Коммунальные: эл-во, вода, газ.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        idents = '&nbsp;&nbsp;&nbsp;&nbsp;' * (self.depth - 1)
        return mark_safe('{}{}'.format(idents, self.name))


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, default=TRANSACTION_EXPENSE)
    date = models.DateField('Дата')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.PROTECT)
    quantity = models.FloatField('Кол-во')
    unit = models.IntegerField('Ед.изм.', choices=UNIT_CHOICES)
    price = models.FloatField('Цена за ед.изм.', blank=True, null=True)
    amount = models.FloatField('Сумма')
    comment = models.TextField('Комментарий', blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_NORMAL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', ]
