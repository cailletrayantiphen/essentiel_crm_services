from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from utilisateur.models import Utilisateur
from gestion_commerciale.models import Particulier, Entreprise, Opportunite
from catalogue_service.models import Service
from utils.permissions import est_manager_ou_plus, est_administrateur

STATUT_COLORS = {
    'gagnee': '#28a745',  # Vert
    'perdue': '#dc3545',  # Rouge
    'qualification': '#36A2EB',  # Bleu
    'negociation': '#ffc107',  # Jaune
}

@login_required
def dashboard_view(request):
    user = request.user
    context = {}

    if est_manager_ou_plus(user):
        opportunites_qs = Opportunite.objects.all()
    else:
        opportunites_qs = Opportunite.objects.filter(responsable=user)

    opportunites_agg = opportunites_qs.aggregate(
        total_opportunites=Count('id'),
        pipeline_total=Sum('montant', filter=~Q(statut__in=['gagnee', 'perdue'])),
        ca_total=Sum('montant', filter=Q(statut='gagnee'))
    )
    context.update(opportunites_agg)

    total_opportunites = opportunites_agg['total_opportunites']
    opportunites_gagnees = opportunites_qs.filter(statut='gagnee').count()
    taux_conversion = (opportunites_gagnees / total_opportunites) * 100 if total_opportunites > 0 else 0
    context['taux_conversion'] = round(taux_conversion, 2)

    opportunites_par_statut_list = list(opportunites_qs.values('statut').annotate(count=Count('id')))
    for item in opportunites_par_statut_list:
        item['color'] = STATUT_COLORS.get(item['statut'], '#6c757d')

    context['opportunites_par_statut'] = opportunites_par_statut_list

    context['opportunites_recentes'] = opportunites_qs.order_by('-date_creation')[:5]

    if est_manager_ou_plus(user):
        context['vue_manager'] = True
        context['est_administrateur'] = est_administrateur(user)

        nombre_particuliers = Particulier.objects.count()
        nombre_entreprises = Entreprise.objects.count()
        context['nombre_clients'] = nombre_particuliers + nombre_entreprises

        context['services_vendus'] = list(
            Service.objects.filter(opportunites__statut='gagnee')
            .values('nom').annotate(ventes=Count('opportunites__id'))
            .order_by('-ventes')
        )

        context['services_vendus_par_categorie'] = list(
            Service.objects.filter(opportunites__statut='gagnee')
            .values('categorie__nom').annotate(ventes=Count('opportunites__id'))
            .order_by('-ventes')
        )
        return render(request, 'tableau_de_bord/tableau_de_bord_gestion.html', context)

    else:
        context['vue_manager'] = False

        nombre_particuliers = Particulier.objects.filter(responsable=user).count()
        nombre_entreprises = Entreprise.objects.filter(responsable=user).count()
        context['nombre_clients'] = nombre_particuliers + nombre_entreprises

        return render(request, 'tableau_de_bord/tableau_de_bord_commercial.html', context)