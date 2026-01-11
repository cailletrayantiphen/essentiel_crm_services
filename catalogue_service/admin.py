from django.contrib import admin
from .models import Categorie, Service

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'type_tarif', 'categorie', 'actif', 'date_creation')
    search_fields = ('nom', 'description')
    list_filter = ('type_tarif', 'categorie', 'actif')
    date_hierarchy = 'date_creation'