from django.urls import path
from .views import (
    ParticulierListView, ParticulierDetailView, ParticulierCreateView, ParticulierUpdateView, ParticulierDeleteView,
    EntrepriseListView, EntrepriseDetailView, EntrepriseCreateView, EntrepriseUpdateView, EntrepriseDeleteView,
    OpportuniteListView, OpportuniteDetailView, OpportuniteCreateView, OpportuniteUpdateView, OpportuniteDeleteView
)

urlpatterns = [
    path('particuliers/', ParticulierListView.as_view(), name='particulier_list'),
    path('particuliers/create/', ParticulierCreateView.as_view(), name='particulier_create'),
    path('particuliers/<int:pk>/', ParticulierDetailView.as_view(), name='particulier_detail'),
    path('particuliers/<int:pk>/update/', ParticulierUpdateView.as_view(), name='particulier_update'),
    path('particuliers/<int:pk>/delete/', ParticulierDeleteView.as_view(), name='particulier_delete'),

    path('entreprises/', EntrepriseListView.as_view(), name='entreprise_list'),
    path('entreprises/create/', EntrepriseCreateView.as_view(), name='entreprise_create'),
    path('entreprises/<int:pk>/', EntrepriseDetailView.as_view(), name='entreprise_detail'),
    path('entreprises/<int:pk>/update/', EntrepriseUpdateView.as_view(), name='entreprise_update'),
    path('entreprises/<int:pk>/delete/', EntrepriseDeleteView.as_view(), name='entreprise_delete'),

    path('opportunites/', OpportuniteListView.as_view(), name='opportunite_list'),
    path('opportunites/create/', OpportuniteCreateView.as_view(), name='opportunite_create'),
    path('opportunites/<int:pk>/', OpportuniteDetailView.as_view(), name='opportunite_detail'),
    path('opportunites/<int:pk>/update/', OpportuniteUpdateView.as_view(), name='opportunite_update'),
    path('opportunites/<int:pk>/delete/', OpportuniteDeleteView.as_view(), name='opportunite_delete'),
]