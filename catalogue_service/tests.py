from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group
from utilisateur.models import Utilisateur, Role
from .models import Categorie, Service
from .forms import CategorieForm, ServiceForm
from decimal import Decimal

class CatalogueServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Création des utilisateurs et des groupes
        Group.objects.get_or_create(name='Administrateur')
        Group.objects.get_or_create(name='Manager')
        Group.objects.get_or_create(name='Commercial')

        cls.admin = Utilisateur.objects.create_user(
            username='admin_user', password='password123', is_superuser=True
        )
        cls.manager = Utilisateur.objects.create_user(
            username='manager_user', password='password123', role=Role.MANAGER
        )
        cls.commercial = Utilisateur.objects.create_user(
            username='commercial_user', password='password123', role=Role.COMMERCIAL
        )
        cls.non_staff_user = Utilisateur.objects.create_user(
            username='simple_user', password='password123'
        )

        # Création des données de test
        cls.categorie1 = Categorie.objects.create(nom="Développement Web")
        cls.categorie2 = Categorie.objects.create(nom="Marketing")

        cls.service1 = Service.objects.create(
            nom="Création de Site Vitrine",
            description="Service de création de site web simple.",
            prix=Decimal('5000.00'),
            type_tarif='FACTURATION_UNIQUE',
            categorie=cls.categorie1,
            actif=True
        )
        cls.service2 = Service.objects.create(
            nom="Abonnement Maintenance",
            description="Contrat de maintenance mensuel.",
            prix=Decimal('500.00'),
            type_tarif='ABONNEMENT_MENSUEL',
            categorie=cls.categorie1,
            actif=True
        )
        cls.service3 = Service.objects.create(
            nom="Consultation SEO",
            description="Audit et conseils SEO.",
            prix=Decimal('1500.00'),
            type_tarif='FACTURATION_UNIQUE',
            categorie=cls.categorie2,
            actif=False
        )

    def setUp(self):
        self.client = Client()

    # --- Tests des permissions de la vue de service ---

    def test_service_list_view_access(self):
        """Vérifie que la liste des services est accessible à tout utilisateur connecté."""
        self.client.login(username='commercial_user', password='password123')
        response = self.client.get(reverse('service_list'))
        self.assertEqual(response.status_code, 200)

    def test_service_create_view_permission(self):
        """Vérifie que seuls les administrateurs peuvent accéder à la création de service."""
        self.client.login(username='commercial_user', password='password123')
        response = self.client.get(reverse('service_create'))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='admin_user', password='password123')
        response = self.client.get(reverse('service_create'))
        self.assertEqual(response.status_code, 200)

    def test_service_update_view_permission(self):
        """Vérifie que seuls les administrateurs peuvent accéder à la modification de service."""
        self.client.login(username='commercial_user', password='password123')
        response = self.client.get(reverse('service_update', args=[self.service1.pk]))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='admin_user', password='password123')
        response = self.client.get(reverse('service_update', args=[self.service1.pk]))
        self.assertEqual(response.status_code, 200)

    # --- Tests de Vues et Logique des formulaires ---

    def test_service_create_view_post_valid_data(self):
        """Vérifie la création d'un service avec des données valides."""
        self.client.login(username='admin_user', password='password123')
        data = {
            'nom': 'Nouveau Service Test',
            'description': 'Description du nouveau service.',
            'prix': '99.99',
            'type_tarif': 'FACTURATION_UNIQUE',
            'categorie': self.categorie1.pk,
            'actif': True
        }
        response = self.client.post(reverse('service_create'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Service.objects.filter(nom='Nouveau Service Test').exists())

    def test_service_update_view_post_valid_data(self):
        """Vérifie la mise à jour d'un service avec des données valides."""
        self.client.login(username='admin_user', password='password123')
        data = {
            'nom': 'Site Vitrine Modifié',
            'description': self.service1.description,
            'prix': '6000.00',
            'type_tarif': self.service1.type_tarif,
            'categorie': self.service1.categorie.pk,
            'actif': self.service1.actif
        }
        response = self.client.post(reverse('service_update', args=[self.service1.pk]), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.service1.refresh_from_db()
        self.assertEqual(self.service1.nom, 'Site Vitrine Modifié')
        self.assertEqual(self.service1.prix, Decimal('6000.00'))

    def test_service_delete_view(self):
        """Vérifie la suppression d'un service."""
        self.client.login(username='admin_user', password='password123')
        response = self.client.post(reverse('service_confirm_delete', args=[self.service1.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Service.objects.filter(pk=self.service1.pk).exists())

    # --- Tests des filtres de la vue de liste ---

    def test_service_filter_by_nom(self):
        """Filtrage des services par nom (recherche insensible à la casse)."""
        self.client.login(username='commercial_user', password='password123')
        response = self.client.get(reverse('service_list'), {'nom': 'vitrine'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['services']), 1)
        self.assertEqual(response.context['services'][0], self.service1)

    def test_service_filter_by_categorie(self):
        """Filtrage des services par catégorie."""
        self.client.login(username='commercial_user', password='password123')
        response = self.client.get(reverse('service_list'), {'categorie': self.categorie2.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['services']), 1)
        self.assertEqual(response.context['services'][0], self.service3)

    def test_service_filter_by_actif_status(self):
        """Filtrage des services par statut actif."""
        self.client.login(username='commercial_user', password='password123')
        response = self.client.get(reverse('service_list'), {'actif': 'False'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['services']), 1)
        self.assertEqual(response.context['services'][0], self.service3)