from django.db import models
import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from stock_exchange.apps.company.manager import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Public identifier',
    )
    email = models.EmailField(max_length=100, unique=True)
    email_verified = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name_plural = "users"

    def __str__(self):
        return f'{self.email}'

    objects = UserManager()


class Company(models.Model):
    """
    Extending User model using one-to-one link
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ref_first_name = models.CharField(max_length=100)
    ref_last_name = models.CharField(max_length=100)
    ref_phone_number = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=100)
    company_symbol = models.CharField(max_length=5)
    website = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    class Meta:
        """Extra model properties."""
        ordering = ['date_added']

    def __str__(self):
        """
        Unicode representation for company model.

        :return: string
        """
        return '{}-{}'.format(str(self.shortened_id), self.company_symbol)

    @property
    def shortened_id(self):
        """Get shortened version of id."""
        return str(self.id)[-8:]
