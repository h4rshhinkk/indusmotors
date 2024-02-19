from core.base import BaseTable

from .models import User
from django_tables2 import columns


class UserTable(BaseTable):
    username = columns.Column(linkify=True)
    date_joined = columns.DateTimeColumn(format="d/m/y")
    created = None

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "usertype",
            "branch",
            "date_joined",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
        )
        attrs = {"class": "table key-buttons border-bottom table-hover"}
