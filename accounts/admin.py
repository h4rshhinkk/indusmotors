from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from import_export.admin import ImportExportActionModelAdmin
from django.forms import CheckboxSelectMultiple
from django.db import models


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError("Username already exists")


class MyUserAdmin(UserAdmin, ImportExportActionModelAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    ordering = ("username",)
    list_display = ("username", "first_name", "usertype", "is_active", "date_joined", "is_staff", "is_superuser")
    list_display_links = ("username",)
    readonly_fields = ("last_login", "date_joined", "pk")
    search_fields = ["branch__branch_name", "username"]
    formfield_overrides = {models.ManyToManyField: {"widget": CheckboxSelectMultiple}}
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined", "last_login", "branch", "usertype")
    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "username",
                    "first_name",
                    "password",
                    "email",
                    "usertype",
                    "branch",
                    "city",
                    "postal_code",
                    "phone",
                    "address",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Groups", {"fields": ("groups",)}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(User, MyUserAdmin)
