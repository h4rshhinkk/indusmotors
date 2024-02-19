from core.base import BaseModel

from django.db import models
from django.urls import reverse_lazy


class Branch(BaseModel):
    branch_id = models.CharField(max_length=128, null=True, blank=True)
    branch_name = models.CharField(max_length=300)
    city = models.CharField(max_length=128, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField("Branch Address", blank=True, null=True)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

    def __str__(self):
        return str(self.branch_name)

    def get_absolute_url(self):
        return reverse_lazy("branches:branch_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("branches:branch_list")

    def get_update_url(self):
        return reverse_lazy("branches:branch_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("branches:branch_delete", kwargs={"pk": self.pk})

    @property
    def fullname(self):
        return self.branch_name
