from django.contrib.auth.models import Group


def default_perm_map(name, user):
    """Get a dict of user object permissions for a given model."""
    app_admin = Group.objects.get(name='app_admin')

    return {
        f'view_{name.lower()}': [user, app_admin],
        f'change_{name.lower()}': [user, app_admin],
        f'delete_{name.lower()}': [user, app_admin]
    }


def get_permissions_map(models: list, user) -> dict:
    """Get a dict of user object permissions for a given list of models."""
    perms = {}
    if isinstance(models, list):
        for name in models:
            perms.update(default_perm_map(name, user))
    return perms
