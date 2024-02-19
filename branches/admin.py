from branches.models import Branch
from core.base import BaseAdmin

from django.contrib import admin


# Register your models here.


@admin.register(Branch)
class BranchAdmin(BaseAdmin):
    list_display = ("branch_name",)
    list_filter = ("is_active",)
    search_fields = ("branch_name",)
    ordering = ("branch_name",)
