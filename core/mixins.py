from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import models as model_forms
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin


class CustomModelFormMixin:
    exclude = None

    # Rewriting get_form_class to support exclude attribute
    def get_form_class(self):
        model = getattr(self, "model", None)
        if self.exclude:
            exclude = getattr(self, "exclude", None)
            return model_forms.modelform_factory(model, exclude=exclude)
        return super().get_form_class()


class HybridDetailView(LoginRequiredMixin, DetailView):
    template_name = "app/common/object_view.html"


class HybridCreateView(LoginRequiredMixin, CustomModelFormMixin, CreateView):
    template_name = "app/common/object_form.html"

    def get_success_url(self):
        return self.object.get_list_url()

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class HybridUpdateView(LoginRequiredMixin, CustomModelFormMixin, UpdateView):
    template_name = "app/common/object_form.html"

    def get_success_url(self):
        return self.object.get_list_url()


class HybridDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "app/common/confirm_delete.html"

    def get_success_url(self):
        return self.object.get_list_url()


class HybridListView(LoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView, ListView):
    table_pagination = {"per_page": 50}
    template_name = "app/common/object_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class HybridFormView(LoginRequiredMixin, FormView):
    pass


class HybridTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "app/common/object_view.html"


class HybridView(LoginRequiredMixin, View):
    pass


class OpenView(TemplateView):
    pass
