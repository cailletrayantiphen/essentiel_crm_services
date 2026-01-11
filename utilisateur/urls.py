from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('connexion/', auth_views.LoginView.as_view(template_name='utilisateur/connexion.html'), name='connexion'),
    path('deconnexion/', auth_views.LogoutView.as_view(), name='deconnexion'),
]