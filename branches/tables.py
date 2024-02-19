from branches.models import Branch
from core.base import BaseTable


class BranchTable(BaseTable):
    class Meta:
        model = Branch
        fields = ("branch_id", "branch_name", "city", "postal_code", "phone")
        attrs = {"class": "table key-buttons border-bottom table-hover"}
