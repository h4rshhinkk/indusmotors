from branches.models import Branch
from core import mixins

from . import tables
from django.urls import reverse_lazy


class BranchListView(mixins.HybridListView):
    model = Branch
    table_class = tables.BranchTable
    filterset_fields = ("branch_name", "branch_id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Branch"
        context["is_branch"] = True
        context["can_add"] = True
        context["new_link"] = reverse_lazy("branches:branch_create")
        return context


class BranchDetailView(mixins.HybridDetailView):
    model = Branch


class BranchCreateView(mixins.HybridCreateView):
    model = Branch
    exclude = ("is_active",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Branch"
        return context


class BranchUpdateView(mixins.HybridUpdateView):
    model = Branch
    exclude = ("is_active",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Branch"
        return context


class BranchDeleteView(mixins.HybridDeleteView):
    model = Branch
