from django.contrib import admin
from .models import Particulier, Entreprise, Opportunite

@admin.register(Particulier)
class ParticulierAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'telephone', 'date_creation', 'date_mise_a_jour')
    search_fields = ('nom', 'prenom', 'email', 'telephone', 'date_creation', 'date_mise_a_jour')
    list_filter = ('date_creation', 'date_mise_a_jour')
    date_hierarchy = 'date_creation'

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('nom_entreprise', 'ice', 'statut_juridique', 'secteur_activite', 'date_creation', 'date_mise_a_jour')
    search_fields = ('nom_entreprise', 'ice', 'email', 'telephone', 'date_creation', 'date_mise_a_jour')
    list_filter = ('statut_juridique', 'secteur_activite', 'date_creation')

@admin.register(Opportunite)
class OpportuniteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'statut', 'responsable', 'client_particulier', 'client_entreprise', 'date_creation', 'date_mise_a_jour')
    list_filter = ('statut', 'responsable', 'date_creation', 'date_mise_a_jour')
    search_fields = ('nom', 'description')
    date_hierarchy = 'date_creation'
    raw_id_fields = ('responsable', 'client_particulier', 'client_entreprise', 'service')