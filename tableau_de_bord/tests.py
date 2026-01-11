from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from gestion_commerciale.models import Particulier, Entreprise, Opportunite, Service
from utilisateur.models import Utilisateur, Role
from decimal import Decimal
from utils.permissions import est_manager_ou_plus, est_administrateur

class DashboardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Création des utilisateurs de test
        cls.admin_user = Utilisateur.objects.create_user(
            username='admin_user', password='password123', is_superuser=True, is_staff=True
        )
        cls.manager_user = Utilisateur.objects.create_user(
            username='manager_user', password='password123', is_staff=True
        )
        cls.commercial_user = Utilisateur.objects.create_user(
            username='commercial_user', password='password123'
        )

        # Création des groupes de rôles (nécessaire pour le modèle Utilisateur)
        Group.objects.get_or_create(name='Administrateur')
        Group.objects.get_or_create(name='Manager')
        Group.objects.get_or_create(name='Commercial')

        # Mise à jour des rôles pour le test et ajout aux groupes
        cls.admin_user.role = Role.ADMIN
        cls.admin_user.save()
        cls.manager_user.role = Role.MANAGER
        cls.manager_user.save()
        cls.commercial_user.role = Role.COMMERCIAL
        cls.commercial_user.save()

        # Création des données de test
        cls.service1 = Service.objects.create(nom="Service A", prix=Decimal('1000.00'))
        cls.service2 = Service.objects.create(nom="Service B", prix=Decimal('5000.00'))
        cls.particulier = Particulier.objects.create(
            nom="Test", prenom="Client", responsable=cls.commercial_user
        )
        cls.entreprise = Entreprise.objects.create(
            nom_entreprise="TestCorp", ice="000000000000001", responsable=cls.commercial_user
        )

        # Création des opportunités pour le commercial
        Opportunite.objects.create(
            nom="Oppo Gagnée", statut="gagnee", responsable=cls.commercial_user,
            service=cls.service1, client_particulier=cls.particulier, montant=cls.service1.prix
        )
        Opportunite.objects.create(
            nom="Oppo Perdue", statut="perdue", responsable=cls.commercial_user,
            service=cls.service2, client_particulier=cls.particulier, montant=cls.service2.prix
        )
        Opportunite.objects.create(
            nom="Oppo Qualification", statut="qualification", responsable=cls.commercial_user,
            service=cls.service1, client_particulier=cls.particulier, montant=cls.service1.prix
        )

        # Création de données pour un autre commercial (pour le test manager)
        autre_commercial = Utilisateur.objects.create_user(username='commercial2', password='123')
        autre_commercial.role = Role.COMMERCIAL
        autre_commercial.save()
        autre_particulier = Particulier.objects.create(nom="Autre", prenom="Client", responsable=autre_commercial)
        Opportunite.objects.create(
            nom="Oppo Gagnée 2", statut="gagnee", responsable=autre_commercial,
            service=cls.service2, client_particulier=autre_particulier, montant=cls.service2.prix
        )

    def test_redirection_unauthenticated_user(self):
        """
        Vérifie qu'un utilisateur non connecté est redirigé vers la page de connexion.
        """
        client_guest = Client()
        response = client_guest.get(reverse('tableau_de_bord'), follow=True)
        self.assertRedirects(response, f"/utilisateur/connexion/?next={reverse('tableau_de_bord')}")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_commercial_view(self):
        """
        Vérifie que la vue du tableau de bord pour un commercial fonctionne correctement.
        """
        self.client.login(username='commercial_user', password='password123')
        response = self.client.get(reverse('tableau_de_bord'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tableau_de_bord/tableau_de_bord_commercial.html')
        self.assertIn('vue_manager', response.context)
        self.assertFalse(response.context['vue_manager'])

        # Vérification des données spécifiques au commercial
        self.assertEqual(response.context['total_opportunites'], 3)
        self.assertEqual(response.context['ca_total'], Decimal('1000.00'))
        self.assertEqual(response.context['pipeline_total'], Decimal('1000.00'))
        self.assertAlmostEqual(response.context['taux_conversion'], 33.33)
        self.assertEqual(response.context['nombre_clients'], 2)

    def test_dashboard_manager_view(self):
        """
        Vérifie que la vue du tableau de bord pour un manager fonctionne correctement.
        """
        self.client.login(username='manager_user', password='password123')
        response = self.client.get(reverse('tableau_de_bord'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tableau_de_bord/tableau_de_bord_gestion.html')
        self.assertIn('vue_manager', response.context)
        self.assertTrue(response.context['vue_manager'])

        # Vérification des données agrégées pour le manager (tous les commerciaux)
        self.assertEqual(response.context['total_opportunites'], 4)
        self.assertEqual(response.context['ca_total'], Decimal('6000.00'))
        self.assertEqual(response.context['pipeline_total'], Decimal('1000.00'))
        self.assertAlmostEqual(response.context['taux_conversion'], 50.00)

    def test_services_vendus_data_manager(self):
        """
        Vérifie que les données sur les services vendus sont correctes pour un manager.
        """
        self.client.login(username='manager_user', password='password123')
        response = self.client.get(reverse('tableau_de_bord'))
        self.assertEqual(response.status_code, 200)

        services_vendus = response.context['services_vendus']
        self.assertEqual(len(services_vendus), 2)

        # Service A a été vendu 1 fois, Service B 1 fois
        self.assertIn({'nom': 'Service A', 'ventes': 1}, services_vendus)
        self.assertIn({'nom': 'Service B', 'ventes': 1}, services_vendus)

    def test_opportunites_par_statut_data(self):
        """
        Vérifie que les données d'opportunités par statut sont correctes.
        """
        self.client.login(username='commercial_user', password='password123')
        response = self.client.get(reverse('tableau_de_bord'))
        self.assertEqual(response.status_code, 200)

        opportunites_par_statut = response.context['opportunites_par_statut']
        self.assertEqual(len(opportunites_par_statut), 3)

        stats_dict = {item['statut']: item['count'] for item in opportunites_par_statut}
        self.assertEqual(stats_dict['gagnee'], 1)
        self.assertEqual(stats_dict['perdue'], 1)
        self.assertEqual(stats_dict['qualification'], 1)
