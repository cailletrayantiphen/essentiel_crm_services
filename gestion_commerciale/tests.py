from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group
from utilisateur.models import Utilisateur, Role
from catalogue_service.models import Service, Categorie
from .models import Particulier, Entreprise, Opportunite, STATUT_OPPORTUNITE_CHOICES
from .forms import ParticulierForm, EntrepriseForm, OpportuniteForm
from decimal import Decimal
from datetime import date
from django.core.exceptions import ValidationError
from utils.permissions import est_commercial_ou_plus, est_manager_ou_plus

class GestionCommercialeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Création des utilisateurs et des groupes
        Group.objects.get_or_create(name='Administrateur')
        Group.objects.get_or_create(name='Manager')
        Group.objects.get_or_create(name='Commercial')

        cls.admin = Utilisateur.objects.create_user(
            username='admin', password='password123', is_superuser=True, is_staff=True
        )
        cls.manager = Utilisateur.objects.create_user(
            username='manager', password='password123', role=Role.MANAGER, is_staff=True
        )
        cls.commercial1 = Utilisateur.objects.create_user(
            username='commercial1', password='password123', role=Role.COMMERCIAL, is_staff=True
        )
        cls.commercial2 = Utilisateur.objects.create_user(
            username='commercial2', password='password123', role=Role.COMMERCIAL, is_staff=True
        )
        # Utilisateur qui n'est ni commercial, ni manager, ni admin
        cls.non_commercial = Utilisateur.objects.create_user(
            username='non_commercial', password='password123', is_staff=False
        )

        # Création des données pour les tests
        cls.categorie = Categorie.objects.create(nom="IT")
        cls.service = Service.objects.create(
            nom="Développement Web", prix=Decimal('10000.00'), categorie=cls.categorie
        )

        cls.particulier1 = Particulier.objects.create(
            civilite='M', nom='Doe', prenom='John', email='john.doe@example.com',
            telephone='+212600000000', date_de_naissance=date(1990, 1, 1),
            adresse='123 Rue de la Liberté', ville='Casablanca', code_postal='20000',
            pays='Maroc', responsable=cls.commercial1
        )
        cls.particulier2 = Particulier.objects.create(
            civilite='Mme', nom='Dupont', prenom='Marie', email='marie.dupont@example.com',
            telephone='+212600000001', date_de_naissance=date(1985, 5, 20),
            adresse='456 Avenue Royale', ville='Rabat', code_postal='10000',
            pays='Maroc', responsable=cls.commercial2
        )

        cls.entreprise1 = Entreprise.objects.create(
            nom_entreprise='Tech Solutions', ice='000000000000001',
            statut_juridique='SARL', secteur_activite='A', email='contact@tech.com',
            telephone='+212500000001', adresse='789 Boulevard Hassan II', ville='Casablanca',
            code_postal='20000', pays='Maroc', responsable=cls.commercial1
        )
        cls.entreprise2 = Entreprise.objects.create(
            nom_entreprise='Innovate Co', ice='000000000000002',
            statut_juridique='SA', secteur_activite='B', email='info@innovate.com',
            telephone='+212500000002', adresse='101 Avenue des F.A.R.', ville='Rabat',
            code_postal='10000', pays='Maroc', responsable=cls.commercial2
        )

        cls.opportunite_gagnee = Opportunite.objects.create(
            nom="Projet Web",
            statut="gagnee",
            responsable=cls.commercial1,
            client_particulier=cls.particulier1,
            service=cls.service
        )
        cls.opportunite_negociation = Opportunite.objects.create(
            nom="Audit SI",
            statut="negociation",
            responsable=cls.commercial1,
            client_entreprise=cls.entreprise1,
            service=cls.service
        )
        cls.opportunite_perdue = Opportunite.objects.create(
            nom="Refonte site",
            statut="perdue",
            responsable=cls.commercial1,
            client_particulier=cls.particulier1,
            service=cls.service
        )

    def setUp(self):
        self.client = Client()

    # --- Tests de Vues et Permissions ---

    def test_particulier_list_view_permission(self):
        """Vérifie que seuls les utilisateurs autorisés peuvent accéder à la liste des particuliers."""
        # Utilisateur non authentifié doit être redirigé vers la page de connexion
        response = self.client.get(reverse('particulier_list'))
        self.assertRedirects(response, f'/utilisateur/connexion/?next={reverse("particulier_list")}')

        # Utilisateur non autorisé (non commercial) doit obtenir un 403
        self.client.login(username='non_commercial', password='password123')
        response = self.client.get(reverse('particulier_list'))
        self.assertEqual(response.status_code, 403)

        # Utilisateur autorisé (commercial) doit obtenir un 200
        self.client.login(username='commercial1', password='password123')
        response = self.client.get(reverse('particulier_list'))
        self.assertEqual(response.status_code, 200)

    # --- Autres tests de vues (à compléter selon votre projet) ---

    # --- Tests des filtres ---

    def test_particulier_filter_manager_user(self):
        """Un manager peut filtrer par responsable."""
        self.client.login(username='manager', password='password123')
        response = self.client.get(reverse('particulier_list') + f'?responsable={self.commercial1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['particuliers']), 1)
        self.assertEqual(response.context['particuliers'][0], self.particulier1)
        self.assertIn('responsable', response.context['filter'].filters)

    def test_particulier_filter_commercial_user_no_responsable(self):
        """Un commercial ne peut pas filtrer par responsable."""
        self.client.login(username='commercial1', password='password123')
        # Crée un objet HttpRequest factice
        request = self.client.get(reverse('particulier_list'))
        # Attache l'utilisateur à la requête
        request.user = self.commercial1
        response = self.client.get(reverse('particulier_list') + '?responsable=1')
        self.assertEqual(response.status_code, 200)
        self.assertFalse('responsable' in response.context['filter'].filters)
        # S'assure que le queryset ne contient que ses propres clients
        self.assertEqual(len(response.context['particuliers']), 1)
        self.assertEqual(response.context['particuliers'][0], self.particulier1)

    def test_particulier_filter_by_nom(self):
        """Filtrage de particuliers par nom."""
        self.client.login(username='commercial1', password='password123')
        response = self.client.get(reverse('particulier_list') + '?nom=doe')
        self.assertEqual(len(response.context['particuliers']), 1)
        self.assertEqual(response.context['particuliers'][0], self.particulier1)

    # --- Tests de logique des modèles ---

    def test_opportunite_creation_updates_montant(self):
        """La création d'une opportunité met à jour le montant avec le prix du service."""
        nouvelle_opportunite = Opportunite.objects.create(
            nom="Nouveau Projet",
            statut="negociation",
            responsable=self.commercial1,
            client_particulier=self.particulier1,
            service=self.service
        )
        self.assertEqual(nouvelle_opportunite.montant, self.service.prix)

    def test_opportunite_gagne_updates_relation_type(self):
        """Le statut 'gagnée' d'une opportunité met à jour le type de relation du client."""
        # Type de relation initial : 'prospect'
        self.assertEqual(self.particulier1.type_relation, 'prospect')

        # Création d'une opportunité gagnée
        Opportunite.objects.create(
            nom="Projet Gagné",
            statut="gagnee",
            responsable=self.commercial1,
            client_particulier=self.particulier1,
            service=self.service
        )
        self.particulier1.refresh_from_db()
        self.assertEqual(self.particulier1.type_relation, 'client')

    def test_opportunite_clean_one_client_only(self):
        """Une opportunité ne peut avoir qu'un seul client ou aucun."""
        # Tentative de créer une opportunité avec les deux clients
        with self.assertRaises(ValidationError):
            Opportunite(
                nom="Erreur",
                statut="negociation",
                responsable=self.commercial1,
                client_particulier=self.particulier1,
                client_entreprise=self.entreprise1,
                service=self.service
            ).clean()

        # Tentative de créer une opportunité sans client
        with self.assertRaises(ValidationError):
            Opportunite(
                nom="Erreur 2",
                statut="negociation",
                responsable=self.commercial1,
                service=self.service
            ).clean()

    # --- Tests de formulaires ---

    def test_opportunite_form_client_filter_manager(self):
        """Le formulaire d'opportunité pour un manager affiche tous les clients."""
        request = self.client.get(reverse('opportunite_list'))
        request.user = self.manager
        form = OpportuniteForm(request=request)
        self.assertEqual(form.fields['client_particulier'].queryset.count(), 2)
        self.assertEqual(form.fields['client_entreprise'].queryset.count(), 2)

    def test_opportunite_form_client_filter_commercial(self):
        """Le formulaire d'opportunité pour un commercial ne montre que ses propres clients."""
        request = self.client.get(reverse('opportunite_list'))
        request.user = self.commercial1
        form = OpportuniteForm(request=request)
        self.assertEqual(form.fields['client_particulier'].queryset.count(), 1)
        self.assertEqual(form.fields['client_entreprise'].queryset.count(), 1)
        self.assertIn(self.particulier1, form.fields['client_particulier'].queryset)