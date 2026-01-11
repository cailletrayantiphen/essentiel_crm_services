import django_filters
from django import forms
from .models import Particulier, Entreprise, Opportunite
from django.contrib.auth import get_user_model
from utils.permissions import est_manager_ou_plus
from catalogue_service.models import Service

User = get_user_model()

class ResponsableFilter(django_filters.ModelChoiceFilter):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class ParticulierFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(
        field_name='nom',
        lookup_expr='icontains',
        label='Nom du Particulier',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher par nom'})
    )
    prenom = django_filters.CharFilter(
        field_name='prenom',
        lookup_expr='icontains',
        label='Prénom du Particulier',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher par prénom'})
    )
    civilite = django_filters.ChoiceFilter(
        field_name='civilite',
        choices=Particulier.civilite.field.choices,
        label='Civilité',
        empty_label='Toutes les civilités',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    type_relation = django_filters.ChoiceFilter(
        field_name='type_relation',
        choices=Particulier.type_relation.field.choices,
        label='Type de Relation',
        empty_label='Tous les types',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    responsable = ResponsableFilter(
        queryset=User.objects.all(),
        empty_label='Tous les responsables',
        label='Responsable',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_creation = django_filters.DateFromToRangeFilter(
        field_name='date_creation',
        label='Date de Création (de / à)',
        widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'JJ/MM/AAAA', 'class': 'form-control'})
    )
    date_mise_a_jour = django_filters.DateFromToRangeFilter(
        field_name='date_mise_a_jour',
        label='Dernière Mise à Jour (de / à)',
        widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'JJ/MM/AAAA', 'class': 'form-control'})
    )

    class Meta:
        model = Particulier
        fields = [
            'nom', 'prenom', 'civilite', 'type_relation', 'responsable',
            'date_creation', 'date_mise_a_jour'
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request and not est_manager_ou_plus(request.user):
            if 'responsable' in self.filters:
                del self.filters['responsable']

class EntrepriseFilter(django_filters.FilterSet):
    nom_entreprise = django_filters.CharFilter(
        field_name='nom_entreprise',
        lookup_expr='icontains',
        label='Nom de l\'Entreprise',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher par nom'})
    )
    ice = django_filters.CharFilter(
        field_name='ice',
        lookup_expr='icontains',
        label='ICE',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher par ICE'})
    )
    statut_juridique = django_filters.ChoiceFilter(
        field_name='statut_juridique',
        choices=Entreprise.statut_juridique.field.choices,
        label='Statut juridique',
        empty_label='Tous les statuts',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    secteur_activite = django_filters.ChoiceFilter(
        field_name='secteur_activite',
        choices=Entreprise.secteur_activite.field.choices,
        label='Secteur d\'Activité',
        empty_label='Tous les secteurs',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    type_compte = django_filters.ChoiceFilter(
        field_name='type_compte',
        choices=Entreprise.type_compte.field.choices,
        label='Type de Compte',
        empty_label='Tous les types',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    nombre_employes = django_filters.ChoiceFilter(
        field_name='nombre_employes',
        choices=Entreprise.nombre_employes.field.choices,
        label='Nombre d\'Employés',
        empty_label='Tous les nombres',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    responsable = ResponsableFilter(
        queryset=User.objects.all(),
        empty_label='Tous les responsables',
        label='Responsable',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_creation = django_filters.DateFromToRangeFilter(
        field_name='date_creation',
        label='Date de Création (de / à)',
        widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'JJ/MM/AAAA', 'class': 'form-control'})
    )
    date_mise_a_jour = django_filters.DateFromToRangeFilter(
        field_name='date_mise_a_jour',
        label='Dernière Mise à Jour (de / à)',
        widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'JJ/MM/AAAA', 'class': 'form-control'})
    )

    class Meta:
        model = Entreprise
        fields = [
            'nom_entreprise', 'ice', 'statut_juridique', 'secteur_activite',
            'type_compte', 'nombre_employes', 'responsable', 'date_creation',
            'date_mise_a_jour'
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request and not est_manager_ou_plus(request.user):
            if 'responsable' in self.filters:
                del self.filters['responsable']

class OpportuniteFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(
        field_name='nom',
        lookup_expr='icontains',
        label='Nom de l\'opportunité',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher par nom'})
    )
    statut = django_filters.ChoiceFilter(
        field_name='statut',
        choices=Opportunite.statut.field.choices,
        empty_label='Tous les statuts',
        label='Statut',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    responsable = ResponsableFilter(
        queryset=User.objects.all(),
        empty_label='Tous les responsables',
        label='Responsable',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    client_particulier = django_filters.ModelChoiceFilter(
        queryset=Particulier.objects.all(),
        label='Client Particulier',
        empty_label='Tous les particuliers',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    client_entreprise = django_filters.ModelChoiceFilter(
        queryset=Entreprise.objects.all(),
        label='Client Entreprise',
        empty_label='Toutes les entreprises',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    service = django_filters.ModelChoiceFilter(
        queryset=Service.objects.all(),
        label='Service',
        empty_label='Tous les services',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_creation = django_filters.DateFromToRangeFilter(
        field_name='date_creation',
        label='Date de Création (de / à)',
        widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'JJ/MM/AAAA', 'class': 'form-control'})
    )
    date_mise_a_jour = django_filters.DateFromToRangeFilter(
        field_name='date_mise_a_jour',
        label='Dernière Mise à Jour (de / à)',
        widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'JJ/MM/AAAA', 'class': 'form-control'})
    )

    class Meta:
        model = Opportunite
        fields = [
            'nom', 'statut', 'responsable', 'service', 'client_particulier',
            'client_entreprise', 'date_creation', 'date_mise_a_jour'
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request and not est_manager_ou_plus(request.user):
            if 'responsable' in self.filters:
                del self.filters['responsable']