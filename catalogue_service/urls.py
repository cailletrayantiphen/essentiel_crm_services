from django.urls import path
from .views import (
    ServiceListView, ServiceDetailView, ServiceCreateView,
    ServiceUpdateView, ServiceDeleteView,
    CategorieListView, CategorieDetailView, CategorieCreateView,
    CategorieUpdateView, CategorieDeleteView
)
urlpatterns = [
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('services/creer/', ServiceCreateView.as_view(), name='service_create'),
    path('services/modifier/<int:pk>/', ServiceUpdateView.as_view(), name='service_update'),
    path('services/supprimer/<int:pk>/', ServiceDeleteView.as_view(), name='service_confirm_delete'),

    path('categories/', CategorieListView.as_view(), name='categorie_list'),
    path('categories/<int:pk>/', CategorieDetailView.as_view(), name='categorie_detail'),
    path('categories/creer/', CategorieCreateView.as_view(), name='categorie_create'),
    path('categories/modifier/<int:pk>/', CategorieUpdateView.as_view(), name='categorie_update'),
    path('categories/supprimer/<int:pk>/', CategorieDeleteView.as_view(), name='categorie_confirm_delete'),
]