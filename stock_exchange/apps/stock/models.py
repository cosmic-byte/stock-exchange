from django.db import models
import uuid
from stock_exchange.apps.stock.managers import StockManager


class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('company.Company', related_name='company_stock', on_delete=models.CASCADE)
    open_amount_in_ngn = models.DecimalField(max_digits=100, decimal_places=2)
    high_amount_in_usd = models.DecimalField(max_digits=100, decimal_places=2)
    low_amount_in_usd = models.DecimalField(max_digits=100, decimal_places=2)
    close_amount_in_usd = models.DecimalField(max_digits=100, decimal_places=2)
    volume_amount_in_usd = models.DecimalField(max_digits=100, decimal_places=2)
    deleted = models.BooleanField(default=False)
    data_time = models.DateTimeField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    objects = StockManager()

    class Meta:
        """Extra model properties."""
        ordering = ['date_added']

    def __str__(self):
        """
        Unicode representation for stock model.

        :return: string
        """
        return str(self.shortened_id)

    @property
    def shortened_id(self):
        """Get shortened version of id."""
        return str(self.id)[-8:]

    @property
    def company_name_indexing(self):
        """Company name indexing.
        Used in Elasticsearch indexing.
        """
        return self.company.company_name

    @property
    def company_symbol_indexing(self):
        """Company symbol indexing.
        Used in Elasticsearch indexing.
        """
        return self.company.company_symbol
