from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class Role(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrateur'
    MANAGER = 'MANAGER', 'Manager'
    COMMERCIAL = 'COMMERCIAL', 'Commercial'

class Utilisateur(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.COMMERCIAL
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='utilisateur_groups_set',
        blank=True,
        related_query_name='utilisateur',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='utilisateur_permissions_set',
        blank=True,
        related_query_name='utilisateur_permission',
    )

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip() if full_name.strip() else self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.groups.clear()
        group_name = self.get_role_display()
        try:
            group = Group.objects.get(name=group_name)
            self.groups.add(group)
        except Group.DoesNotExist:
            print(
                f"Attention : le groupe '{group_name}' n'existe pas. Veuillez le créer dans l'administration de Django.")