from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from catalogue_service.models import Service
from django.contrib.auth import get_user_model

User = get_user_model()

CIVILITE_CHOICES = [
    ('M', 'M.'),
    ('Mme', 'Mme'),
]

STATUT_ENTREPRISE_CHOICES = [
    ('SARL', 'SARL - Société à Responsabilité Limitée'),
    ('EURL', 'EURL - Entreprise Unipersonnelle à Responsabilité Limitée'),
    ('SAS', 'SAS - Société par Actions Simplifiée'),
    ('SASU', 'SASU - Société par Actions Simplifiée Unipersonnelle'),
    ('SA', 'SA - Société Anonyme'),
    ('SNC', 'SNC - Société en Nom Collectif'),
    ('SCS', 'SCS - Société en Commandite Simple'),
    ('SCA', 'SCA - Société en Commandite par Actions'),
    ('GIE', 'GIE - Groupement d\'Intérêt Économique'),
    ('Micro-entreprise', 'Micro-entreprise'),
    ('Association', 'Association (Loi 1901)'),
    ('Coopérative', 'Coopérative'),
    ('SCI', 'SCI - Société Civile Immobilière'),
    ('SCP', 'SCP - Société Civile Professionnelle'),
    ('Auto-entrepreneur', 'Auto-entrepreneur (ancien statut)'),
    ('Autre', 'Autre'),
]

SECTEUR_ACTIVITE_CHOICES = [
    ('A', 'Agriculture, Sylviculture et Pêche'),
    ('B', 'Industries Extractives'),
    ('C', 'Industrie manufacturière'),
    ('D', 'Production et distribution d’eau et d’électricité'),
    ('E', 'Bâtiment et travaux publics (BTP)'),
    ('F', 'Commerce de gros et de détail'),
    ('G', 'Transports, entreposage et communications'),
    ('H', 'Services aux entreprises'),
    ('I', 'Services aux particuliers'),
    ('J', 'Enseignement, santé et action sociale'),
    ('K', 'Services publics'),
    ('L', 'Hébergement et restauration'),
    ('M', 'Activités financières et d’assurance'),
    ('N', 'Activités immobilières'),
    ('O', 'Autres activités de services'),
]

STATUT_OPPORTUNITE_CHOICES = [
    ('qualification', 'Qualification'),
    ('negociation', 'Négociation'),
    ('gagnee', 'Gagnée'),
    ('perdue', 'Perdue'),
]

SOURCE_CHOICES = [
    ('telephone', 'Appel Téléphonique'),
    ('web', 'Site Web'),
    ('recommandation', 'Recommandation'),
    ('salon', 'Salon ou Événement'),
    ('reseaux_sociaux', 'Réseaux Sociaux'),
    ('autre', 'Autre'),
]

NOMBRE_EMPLOYES_CHOICES = [
    ('micro', 'Moins de 10 employés (Micro-entreprise)'),
    ('petite', '10 à 49 employés (Petite Entreprise)'),
    ('moyenne', '50 à 249 employés (Moyenne Entreprise)'),
    ('grande', '250 employés ou plus (Grande Entreprise)'),
]

PRIORITE_CHOICES = [
    ('faible', 'Faible'),
    ('moyenne', 'Moyenne'),
    ('haute', 'Haute'),
]

TYPE_RELATION_CHOICES = [
    ('prospect', 'Prospect'),
    ('client', 'Client'),
]


class BaseModelTracking(models.Model):
    date_creation = models.DateTimeField(
        auto_now_add=True,
        help_text="Date et heure de création de l'enregistrement."
    )
    date_mise_a_jour = models.DateTimeField(
        auto_now=True,
        help_text="Date et heure de modification de l'enregistrement."
    )

    class Meta:
        abstract = True


class BaseContactInfo(models.Model):
    email = models.EmailField(
        unique=True,
        help_text="Adresse e-mail unique du contact."
    )
    telephone = PhoneNumberField(
        unique=True,
        help_text="Numéro de téléphone unique du contact."
    )
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        blank=True,
        help_text="Source d'où provient ce contact (ex: site web, Appel téléphonique)."
    )
    notes_supplementaires = models.TextField(
        blank=True,
        help_text="Notes internes ou informations supplémentaires concernant le contact."
    )

    class Meta:
        abstract = True


class BaseAdresseInfo(models.Model):
    adresse = models.TextField(
        help_text="Adresse complète (rue, numéro, etc.)."
    )
    ville = models.CharField(
        max_length=100,
        help_text="Ville de résidence ou du siège social."
    )
    code_postal = models.CharField(
        max_length=10,
        help_text="Code postal de l'adresse.")
    pays = models.CharField(
        max_length=100,
        help_text="Pays de l'adresse."
    )

    class Meta:
        abstract = True


class Particulier(BaseModelTracking, BaseAdresseInfo, BaseContactInfo):
    civilite = models.CharField(
        max_length=5,
        choices=CIVILITE_CHOICES,
        help_text="Civilité du client (M., Mme)."
    )
    nom = models.CharField(
        max_length=100,
        help_text="Nom de famille du client."
    )
    prenom = models.CharField(
        max_length=100,
        help_text="Prénom du client."
    )
    date_de_naissance = models.DateField(
        help_text="Date de naissance du client."
    )
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='particuliers_geres',
        help_text="Utilisateur responsable de ce client particulier."
    )
    type_relation = models.CharField(
        max_length=20,
        choices=TYPE_RELATION_CHOICES,
        default='prospect',
        help_text="Le type de relation avec ce particulier."
    )

    class Meta:
        verbose_name = "Particulier"
        verbose_name_plural = "Particuliers"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def update_relation_type(self):
        gagné_count = self.opportunites_particulier.filter(statut='gagnee').count()
        if gagné_count >= 1:
            self.type_relation = 'client'
        else:
            self.type_relation = 'prospect'
            self.save()


class Entreprise(BaseModelTracking, BaseAdresseInfo, BaseContactInfo):
    ice = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            MinLengthValidator(15),
            MaxLengthValidator(15),
            RegexValidator(r'^\d{15}$', 'L\'ICE doit contenir exactement 15 chiffres.')
        ],
        verbose_name="ICE",
        help_text="Identifiant Commun de l'Entreprise (15 chiffres). Obligatoire."
    )
    statut_juridique = models.CharField(
        max_length=32,
        choices=STATUT_ENTREPRISE_CHOICES,
        help_text="Forme juridique de l'entreprise (ex: SARL, SA, etc.)."
    )
    secteur_activite = models.CharField(
        max_length=45,
        choices=SECTEUR_ACTIVITE_CHOICES,
        help_text="Secteur d'activité principal de l'entreprise selon la nomenclature marocaine (NAM)."
    )
    nom_entreprise = models.CharField(
        max_length=200,
        unique=True,
        help_text="Nom légal de l'entreprise."
    )
    website = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Site Web",
        help_text="Adresse du site web de l'entreprise."
    )
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entreprises_gerees',
        help_text="Utilisateur responsable de cette entreprise."
    )
    contact_principal = models.ForeignKey(
        Particulier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Personne de contact principale au sein de l'entreprise."
    )
    nombre_employes = models.CharField(
        max_length=10,
        choices=NOMBRE_EMPLOYES_CHOICES,
        blank=True,
        help_text="Tranche du nombre d'employés dans l'entreprise selon la classification européenne."
    )
    type_compte = models.CharField(
        max_length=20,
        choices=TYPE_RELATION_CHOICES,
        default='prospect',
        help_text="Le type de relation avec cette entreprise."
    )

    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"
        ordering = ['nom_entreprise']

    def __str__(self):
        return self.nom_entreprise

    def update_relation_type(self):
        gagné_count = self.opportunites_entreprise.filter(statut='gagnee').count()
        if gagné_count >= 1:
            self.type_compte = 'client'
        else:
            self.type_compte = 'prospect'
            self.save()


class Opportunite(BaseModelTracking):
    nom = models.CharField(
        max_length=200,
        unique=True,
        help_text="Nom court pour l'opportunité."
    )
    description = models.TextField(
        blank=True,
        help_text="Description détaillée de ce que l'opportunité implique."
    )
    statut = models.CharField(
        max_length=13,
        choices=STATUT_OPPORTUNITE_CHOICES,
        help_text="Statut actuel de l'opportunité dans le processus de vente."
    )
    montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Montant total de l'opportunité, mis à jour automatiquement."
    )
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='opportunites_gerees',
        help_text="Utilisateur responsable du suivi de cette opportunité."
    )
    client_particulier = models.ForeignKey(
        'Particulier',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='opportunites_particulier',
        help_text="Client particulier associé à cette opportunité."
    )
    client_entreprise = models.ForeignKey(
        'Entreprise',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='opportunites_entreprise',
        help_text="Client entreprise associé à cette opportunité."
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        related_name='opportunites',
        verbose_name="Service associé",
        help_text="Le service ou produit unique inclus dans cette opportunité."
    )

    def save(self, *args, **kwargs):
        if self.service:
            self.montant = self.service.prix
            super().save(*args, **kwargs)
        if self.statut == 'gagnee':
            if self.client_particulier:
                self.client_particulier.update_relation_type()
            if self.client_entreprise:
                self.client_entreprise.update_relation_type()

    class Meta:
        verbose_name = "Opportunité"
        verbose_name_plural = "Opportunités"
        ordering = ['-date_creation']

    def clean(self):
        if not (self.client_particulier or self.client_entreprise):
            raise ValidationError("Une opportunité doit être associée à un client (particulier ou entreprise).")
        if self.client_particulier and self.client_entreprise:
            raise ValidationError(
                "Une opportunité ne peut être associée qu'à un seul client (particulier ou entreprise).")

    def __str__(self):
        return self.nom