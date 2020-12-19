from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from rest_framework.generics import get_object_or_404


class UserManager(BaseUserManager):

    def create_base_user(self, email=None, password=None, **extra_fields):
        if not email or not password:
            raise ValueError('The email and password must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_app_admin_user(self, email=None, password=None, user=None, **extra_fields):
        if not user:
            user = self.create_base_user(email=email, password=password, **extra_fields)
        admin = get_object_or_404(Group, name='app_admin')
        user.groups.add(admin)
        return user

    def create_company_user(self, email=None, password=None, user=None, **extra_fields):
        if not user:
            user = self.create_base_user(email=email, password=password, **extra_fields)
        client = get_object_or_404(Group, name='company')
        user.groups.add(client)
        return user

    def create_superuser(self, email, password, user=None, **extra_fields):
        if not user:
            user = self.create_base_user(email=email, password=password, **extra_fields)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
