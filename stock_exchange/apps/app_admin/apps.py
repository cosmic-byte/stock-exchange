from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db.models import Q


def perform_permission_assignment(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from stock_exchange.apps.company.models import User

    admin_group, _ = Group.objects.get_or_create(name='app_admin')
    company_group, _ = Group.objects.get_or_create(name='company')

    permissions_exists = company_group.permissions.exists()

    if not permissions_exists:
        model_names = ['company', 'stock']

        def get_perm_filters(perm):
            return [f'{perm}_{name}' for name in model_names]

        perms = [
            *get_perm_filters('add'),
            *get_perm_filters('change'),
            *get_perm_filters('view'),
            *get_perm_filters('delete')
        ]

        # Assign model permissions to company group
        permissions = Permission.objects.filter(
            Q(codename__in=perms, content_type__app_label='company') |
            Q(codename__in=perms, content_type__app_label='stock')
        )
        [company_group.permissions.add(p) for p in permissions]

        # Assign all permissions to app_admin group
        [admin_group.permissions.add(p) for p in Permission.objects.all()]

    # create superuser
    admin_user = User.objects.filter(email='admin@admin.com').exists()
    if not admin_user:
        User.objects.create_superuser(email='admin@admin.com', password='password')


class AdminConfig(AppConfig):
    name = 'stock_exchange.apps.app_admin'

    def ready(self):
        post_migrate.connect(perform_permission_assignment, sender=self)
