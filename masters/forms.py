from django import forms
from masters.models import Stock


class PdiupdatestockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ("dealer_location", "display_status")
