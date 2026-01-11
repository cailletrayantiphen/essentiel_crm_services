# 🚀 Essentiel CRM Services

Une solution robuste de gestion de la relation client (CRM) et de suivi commercial développée avec le framework **Django**.

## 📋 Présentation
Ce projet vise à automatiser les processus commerciaux d'une structure de services. Il permet de centraliser la gestion des clients, le catalogue des prestations et le suivi rigoureux des réalisations.

## ✨ Fonctionnalités Principales
- **Dashboard Analytique :** Visualisation des indicateurs clés (KPI) via des graphiques dynamiques intégrés (Chart.js).
- **Filtrage & Recherche Avancée :** Système de recherche multi-critères permettant d'extraire précisément les données (clients, services, opportunités) selon des paramètres spécifiques (date, catégorie, statut, responsable, type de tarifications etc).
- **Gestion Commerciale :** Cycle complet de vente, de la fiche client à la validation des prestations.
- **Sécurité & Rôles :** Accès sécurisé avec gestion fine des permissions (Admin, Manager, Commercial, Administrateur-système).

## 🛠 Stack Technique
- **Backend :** Python 3.x, Django 4.2+
- **Base de données :** PostgreSQL (Production)
- **Frontend :** JavaScript, Bootstrap 5, HTML5/CSS3, Chart.js
- **Outils :** Git, PyCharm, venv
  
## ⚙️ Installation Rapide
1. Cloner le projet :
\\\`bash
git clone [https://github.com/cailletrayantiphen/essentiel_crm_services.git](https://github.com/cailletrayantiphen/essentiel_crm_services.git)
\\\`

2. Installer les dépendances :
\\\`bash
pip install -r requirements.txt
\\\`

3. Lancer les migrations :
\\\`bash
python manage.py migrate
\\\`

4. Démarrer le serveur :
\\\`bash
python manage.py runserver
