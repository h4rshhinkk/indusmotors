from core.functions import generate_fields

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy


class User(AbstractUser):
    usertype = models.CharField(
        max_length=128,
        choices=[
            ("customer_advisor", "Customer Advisor"),
            ("team_lead", "Team Lead"),
            ("asm", "Area Sales Manager"),
            ("sm", "Sales Manager"),
            ("gm", "General Manager"),
            ("accounts", "Accounts"),
            ("pdi", "PDI"),
            ("registration_bo", "Registration BO"),
            ("exchange_bo", "Exchange BO"),
            ("tmga", "TMGA"),
            ("insurance", "Insurance"),
            ("scheme", "Scheme"),
            ("finance_bo", "Finance BO"),
            ("finance_executive", "Finance Executive"),
            ("stock", "Stock"),
            ("invoice_team", "Invoice Team"),
            ("deo", "Data Entry Operator"),
            ("post_sales_followup", "Post Sales Followup"),
            ("test_drive_operator", "Test Drive Operator"),
            ("cre", "CRE"),
            ("digital_lead", "Digital Lead"),
        ],
        default="customer_advisor",
    )
    branch = models.ManyToManyField("branches.Branch", blank=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def get_fields(self):
        return generate_fields(self)

    def get_absolute_url(self):
        return reverse_lazy("accounts:user_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("accounts:user_list")

    def get_update_url(self):
        return reverse_lazy("accounts:user_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("accounts:user_delete", kwargs={"pk": self.pk})

    @property
    def fullname(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.username

    def __str__(self):
        return self.fullname
