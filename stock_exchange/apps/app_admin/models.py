from django.db import models

from stock_exchange.apps.company.models import User
from stock_exchange.apps.app_admin.managers import AdminManager


class AppAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_by', null=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = AdminManager()

    def __str__(self):
        return f'{self.first_name}'
