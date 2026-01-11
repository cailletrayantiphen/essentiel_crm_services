from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Particulier, Entreprise, Opportunite
from .forms import ParticulierForm, EntrepriseForm, OpportuniteForm
from .filters import ParticulierFilter, EntrepriseFilter, OpportuniteFilter
from utils.permissions import est_commercial_ou_plus, est_manager_ou_plus

class ParticulierListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Particulier
    template_name = 'gestion_commerciale/particulier_list.html'
    context_object_name = 'particuliers'

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()

        if not est_manager_ou_plus(self.request.user):
            queryset = queryset.filter(responsable=self.request.user)

        self.filterset = ParticulierFilter(self.request.GET, queryset=queryset, request=self.request)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['total_particuliers'] = self.get_queryset().count()
        context['peut_voir_responsable'] = est_manager_ou_plus(self.request.user)
        return context

class ParticulierDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Particulier
    template_name = 'gestion_commerciale/particulier_detail.html'

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['peut_voir_responsable'] = est_manager_ou_plus(self.request.user)
        return context

class ParticulierCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Particulier
    form_class = ParticulierForm
    template_name = 'gestion_commerciale/particulier_form.html'
    success_url = reverse_lazy('particulier_list')

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

    def form_valid(self, form):
        form.instance.responsable = self.request.user
        return super().form_valid(form)

class ParticulierUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Particulier
    form_class = ParticulierForm
    template_name = 'gestion_commerciale/particulier_form.html'
    success_url = reverse_lazy('particulier_list')

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

class ParticulierDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Particulier
    template_name = 'gestion_commerciale/particulier_confirm_delete.html'
    success_url = reverse_lazy('particulier_list')

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

class EntrepriseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Entreprise
    template_name = 'gestion_commerciale/entreprise_list.html'
    context_object_name = 'entreprises'

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()

        if not est_manager_ou_plus(self.request.user):
            queryset = queryset.filter(responsable=self.request.user)

        self.filterset = EntrepriseFilter(self.request.GET, queryset=queryset, request=self.request)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['total_entreprises'] = self.get_queryset().count()
        context['peut_voir_responsable'] = est_manager_ou_plus(self.request.user)
        return context

class EntrepriseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Entreprise
    template_name = 'gestion_commerciale/entreprise_detail.html'

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['peut_voir_responsable'] = est_manager_ou_plus(self.request.user)
        return context

class EntrepriseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = 'gestion_commerciale/entreprise_form.html'
    success_url = reverse_lazy('entreprise_list')

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

    def form_valid(self, form):
        form.instance.responsable = self.request.user
        return super().form_valid(form)

class EntrepriseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = 'gestion_commerciale/entreprise_form.html'
    success_url = reverse_lazy('entreprise_list')

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

class EntrepriseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entreprise
    template_name = 'gestion_commerciale/entreprise_confirm_delete.html'
    success_url = reverse_lazy('entreprise_list')

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

class OpportuniteListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Opportunite
    template_name = 'gestion_commerciale/opportunite_list.html'
    context_object_name = 'opportunites'

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()

        if not est_manager_ou_plus(self.request.user):
            queryset = queryset.filter(responsable=self.request.user)

        self.filterset = OpportuniteFilter(self.request.GET, queryset=queryset, request=self.request)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['total_opportunites'] = self.get_queryset().count()
        context['peut_voir_responsable'] = est_manager_ou_plus(self.request.user)
        return context

class OpportuniteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Opportunite
    template_name = 'gestion_commerciale/opportunite_detail.html'

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['peut_voir_responsable'] = est_manager_ou_plus(self.request.user)
        return context

class OpportuniteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Opportunite
    form_class = OpportuniteForm
    template_name = 'gestion_commerciale/opportunite_form.html'
    success_url = reverse_lazy('opportunite_list')

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.responsable = self.request.user
        return super().form_valid(form)

class OpportuniteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Opportunite
    form_class = OpportuniteForm
    template_name = 'gestion_commerciale/opportunite_form.html'
    success_url = reverse_lazy('opportunite_list')

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class OpportuniteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Opportunite
    template_name = 'gestion_commerciale/opportunite_confirm_delete.html'
    success_url = reverse_lazy('opportunite_list')

    def test_func(self):
        return est_commercial_ou_plus(self.request.user)