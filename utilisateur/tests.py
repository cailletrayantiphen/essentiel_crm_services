from django.test import TestCase, Client
from django.urls import reverse
from utilisateur.models import Utilisateur, Role

class UtilisateurViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Utilisateur.objects.create_user(
            username='testuser', password='password123'
        )

    def test_connexion_view_access(self):
        response = self.client.get(reverse('connexion'))
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        response = self.client.post(
            reverse('connexion'),
            {'username': 'testuser', 'password': 'password123'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tableau_de_bord'))

    def test_deconnexion(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('deconnexion'), follow=True)
        self.assertRedirects(response, reverse('connexion'))
        self.assertFalse(response.context['user'].is_authenticated)

    def test_failed_login(self):
        response = self.client.post(
            reverse('connexion'),
            {'username': 'testuser', 'password': 'mauvaismotdepasse'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Veuillez entrer un nom d’utilisateur et un mot de passe valides")