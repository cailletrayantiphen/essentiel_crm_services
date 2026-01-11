from django.contrib.auth.models import Group

def est_administrateur(user):
    if not user.is_authenticated:
        return False

    return user.is_superuser or user.groups.filter(name='Administrateur').exists()

def est_manager_ou_plus(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.groups.filter(name__in=['Administrateur', 'Manager']).exists()

def est_commercial_ou_plus(user):
    if not user.is_authenticated:
        return False

    return user.is_superuser or user.groups.filter(name__in=['Administrateur', 'Manager', 'Commercial']).exists()