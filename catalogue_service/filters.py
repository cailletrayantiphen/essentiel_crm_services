import django_filters
from django import forms
from .models import Service, Categorie

class ServiceFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(
        field_name='nom',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher par nom'})
    )
    categorie = django_filters.ModelChoiceFilter(
        field_name='categorie',
        queryset=Categorie.objects.all(),
        empty_label='Toutes les catégories',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    type_tarif = django_filters.ChoiceFilter(
        field_name='type_tarif',
        choices=Service.TypeTarif.choices,
        empty_label='Tous les types de tarif',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    actif = django_filters.BooleanFilter(
        field_name='actif',
        widget=forms.Select(
            attrs={'class': 'form-select'},
            choices=[
                ('', '---------'),
                (True, 'Oui'),
                (False, 'Non'),
            ]
        )
    )

    def __init__(self, *args, **kwargs):
        user_est_administrateur = kwargs.pop('est_administrateur', False)
        super().__init__(*args, **kwargs)

        if user_est_administrateur:
            self.filters['date_creation'] = django_filters.DateFromToRangeFilter(
                field_name='date_creation',
                label='Date de Création (de / à)',
                widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'JJ/MM/AAAA', 'class': 'form-control'})
            )
            self.filters['date_mise_a_jour'] = django_filters.DateFromToRangeFilter(
                field_name='date_mise_a_jour',
                label='Dernière Mise à Jour (de / à)',
                widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'JJ/MM/AAAA', 'class': 'form-control'})
            )

    class Meta:
        model = Service
        fields = ['nom', 'categorie', 'type_tarif', 'actif']

class CategorieFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(
        field_name='nom',
        lookup_expr='icontains',
        label='Nom de la catégorie',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher par nom'})
    )

    def __init__(self, *args, **kwargs):
        user_est_administrateur = kwargs.pop('est_administrateur', False)
        super().__init__(*args, **kwargs)

        if user_est_administrateur:
            self.filters['date_creation'] = django_filters.DateFromToRangeFilter(
                field_name='date_creation',
                label='Date de Création (de / à)',
                widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'JJ/MM/AAAA', 'class': 'form-control'})
            )
            self.filters['date_mise_a_jour'] = django_filters.DateFromToRangeFilter(
                field_name='date_mise_a_jour',
                label='Dernière Mise à Jour (de / à)',
                widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'JJ/MM/AAAA', 'class': 'form-control'})
            )

    class Meta:
        model = Categorie
        fields = ['nom']