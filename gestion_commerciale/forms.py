from django import forms
from .models import Particulier, Entreprise, Opportunite, STATUT_ENTREPRISE_CHOICES, SECTEUR_ACTIVITE_CHOICES, CIVILITE_CHOICES, STATUT_OPPORTUNITE_CHOICES, PRIORITE_CHOICES
from utils.permissions import est_manager_ou_plus

class ParticulierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = None

    class Meta:
        model = Particulier
        fields = ['civilite', 'prenom', 'nom', 'email', 'telephone', 'date_de_naissance', 'adresse', 'ville', 'code_postal', 'pays', 'source', 'notes_supplementaires']
        widgets = {
            'civilite': forms.Select(attrs={'class': 'form-select'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_de_naissance': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'code_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'pays': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'notes_supplementaires': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'civilite': 'Civilité',
            'prenom': 'Prénom',
            'nom': 'Nom',
            'email': 'E-mail',
            'telephone': 'Téléphone',
            'date_de_naissance': 'Date de naissance',
            'adresse': 'Adresse',
            'ville': 'Ville',
            'code_postal': 'Code Postal',
            'pays': 'Pays',
            'source': 'Source',
            'notes_supplementaires': 'Notes supplémentaires',
        }

class EntrepriseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = None

    class Meta:
        model = Entreprise
        fields = ['nom_entreprise', 'ice', 'statut_juridique', 'secteur_activite', 'email', 'telephone', 'website', 'adresse', 'ville', 'code_postal', 'pays', 'contact_principal', 'nombre_employes', 'source', 'notes_supplementaires']
        widgets = {
            'nom_entreprise': forms.TextInput(attrs={'class': 'form-control'}),
            'ice': forms.TextInput(attrs={'class': 'form-control'}),
            'statut_juridique': forms.Select(attrs={'class': 'form-select'}),
            'secteur_activite': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'code_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'pays': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_principal': forms.Select(attrs={'class': 'form-select'}),
            'nombre_employes': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'notes_supplementaires': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'nom_entreprise': 'Nom de l\'entreprise',
            'ice': 'Identifiant Commun des Entreprises (ICE)',
            'statut_juridique': 'Statut Juridique',
            'secteur_activite': 'Secteur d\'Activité',
            'email': 'E-mail',
            'telephone': 'Téléphone',
            'website': 'Site Web',
            'adresse': 'Adresse',
            'ville': 'Ville',
            'code_postal': 'Code Postal',
            'pays': 'Pays',
            'contact_principal': 'Contact Principal',
            'nombre_employes': 'Nombre d\'employés',
            'source': 'Source',
            'notes_supplementaires': 'Notes supplémentaires',
        }


class OpportuniteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request and not est_manager_ou_plus(self.request.user):
            self.fields['client_particulier'].queryset = Particulier.objects.filter(responsable=self.request.user)
            self.fields['client_entreprise'].queryset = Entreprise.objects.filter(responsable=self.request.user)

    class Meta:
        model = Opportunite
        fields = ['nom', 'description', 'statut', 'client_particulier', 'client_entreprise', 'service']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'client_particulier': forms.Select(attrs={'class': 'form-select'}),
            'client_entreprise': forms.Select(attrs={'class': 'form-select'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nom': 'Nom de l\'opportunité',
            'description': 'Description',
            'statut': 'Statut',
            'client_particulier': 'Client Particulier',
            'client_entreprise': 'Client Entreprise',
            'service': 'Service associé',
        }

    def clean(self):
        cleaned_data = super().clean()
        client_particulier = cleaned_data.get('client_particulier')
        client_entreprise = cleaned_data.get('client_entreprise')

        if not client_particulier and not client_entreprise:
            raise forms.ValidationError("Vous devez choisir un client, soit un particulier, soit une entreprise.")

        if client_particulier and client_entreprise:
            raise forms.ValidationError(
                "Vous ne pouvez pas associer l'opportunité à la fois à un particulier et à une entreprise.")

        return cleaned_data