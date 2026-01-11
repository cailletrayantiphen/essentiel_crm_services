from django.db import models

class Categorie(models.Model):
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la catégorie",
        help_text="Nom unique de la catégorie de services (ex : 'Développement Web', 'Marketing Digital')."
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Description détaillée de la catégorie."
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
        help_text="Date à laquelle cette catégorie a été créée."
    )
    date_mise_a_jour = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour",
        help_text="Date de la dernière modification des informations de la catégorie."
    )

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']

    def __str__(self):
        return self.nom

class Service(models.Model):
    class TypeTarif(models.TextChoices):
        ABONNEMENT_MENSUEL = 'ABONNEMENT_MENSUEL', 'Abonnement Mensuel'
        FACTURATION_UNIQUE = 'FACTURATION_UNIQUE', 'Facturation Unique'
        ABONNEMENT_ANNUEL = 'ABONNEMENT_ANNUEL', 'Abonnement Annuel'

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Catégorie",
        help_text="Catégorie à laquelle ce service appartient."
    )
    nom = models.CharField(
        max_length=200,
        verbose_name="Nom du service",
        help_text="Nom du service ou du produit."
    )
    description = models.TextField(
        verbose_name="Description détaillée",
        help_text="Description complète des fonctionnalités et avantages du service."
    )
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix",
        help_text="Prix du service."
    )
    type_tarif = models.CharField(
        max_length=20,
        choices=TypeTarif.choices,
        verbose_name="Type de tarification",
        help_text="Sélectionnez le type de tarification pour ce service."
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Indique si le service est actuellement disponible dans le catalogue."
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
        help_text="Date à laquelle ce service a été ajouté au catalogue."
    )
    date_mise_a_jour = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour",
        help_text="Date de la dernière modification des informations du service."
    )

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['nom']

    def __str__(self):
        return self.nom