from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Service, Categorie
from .forms import ServiceForm, CategorieForm
from .filters import ServiceFilter, CategorieFilter
from utils.permissions import est_administrateur

class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'catalogue_service/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = ServiceFilter(self.request.GET, queryset=queryset,
                                    est_administrateur=est_administrateur(self.request.user))
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        context['total_services'] = self.filter.qs.count()
        context['est_administrateur'] = est_administrateur(self.request.user)
        return context

class ServiceDetailView(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'catalogue_service/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['est_administrateur'] = est_administrateur(self.request.user)
        return context

class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'catalogue_service/service_form.html'
    success_url = reverse_lazy('service_list')

    def test_func(self):
        return est_administrateur(self.request.user)

class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'catalogue_service/service_form.html'
    success_url = reverse_lazy('service_list')

    def test_func(self):
        return est_administrateur(self.request.user)

class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Service
    template_name = 'catalogue_service/service_confirm_delete.html'
    success_url = reverse_lazy('service_list')

    def test_func(self):
        return est_administrateur(self.request.user)

class CategorieListView(LoginRequiredMixin, ListView):
    model = Categorie
    template_name = 'catalogue_service/categorie_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CategorieFilter(self.request.GET, queryset=queryset,
                                         est_administrateur=est_administrateur(self.request.user))
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['est_administrateur'] = est_administrateur(self.request.user)
        context['total_categories'] = self.filterset.qs.count()
        return context

class CategorieDetailView(LoginRequiredMixin, DetailView):
    model = Categorie
    template_name = 'catalogue_service/categorie_detail.html'
    context_object_name = 'categorie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['est_administrateur'] = est_administrateur(self.request.user)
        return context

class CategorieCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'catalogue_service/categorie_form.html'
    success_url = reverse_lazy('categorie_list')

    def test_func(self):
        return est_administrateur(self.request.user)

class CategorieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'catalogue_service/categorie_form.html'
    success_url = reverse_lazy('categorie_list')

    def test_func(self):
        return est_administrateur(self.request.user)

class CategorieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Categorie
    template_name = 'catalogue_service/categorie_confirm_delete.html'
    success_url = reverse_lazy('categorie_list')

    def test_func(self):
        return est_administrateur(self.request.user)