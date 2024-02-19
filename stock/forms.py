from django import forms
from crm.models import BookingInvoice
from masters.models import CarModel, Color, District, State, Stock, Trim, Variant
from core.choices import  SELECTION_CHOICES, SELECTION_CHOICES_FINANCE


class BookingInvoiceUpdateFormStock(forms.ModelForm):
    car_model = forms.ModelChoiceField(queryset=CarModel.objects.all())
    trim = forms.ModelChoiceField(queryset=Trim.objects.all())
    color = forms.ModelChoiceField(queryset=Color.objects.all())
    variant = forms.ModelChoiceField(queryset=Variant.objects.all())
    chassis = forms.ModelChoiceField(queryset=Stock.objects.all())

    class Meta:
        model = BookingInvoice
        fields = ("car_model", "trim", "color", "variant", "chassis", "status", "remarks")


class BookingInvoiceUpdateFormInvoice(forms.ModelForm):
    class Meta:
        model = BookingInvoice
        fields = (
            "invoice_date",
            "invoice_no",
            "consumer_offer",
            "consumer_offer_campaign_code",
            "consumer_offer_amount",
            "consumer_dealer_share",
            "consumer_tml_share",
            "isl_scheme",
            "isl_offer_campaign_code",
            "isl_share",
            "isl_dealer_share",
            "total_isl_amount",
            "invoice_scheme_name",
            "invoice_scheme_campaign_code",
            "invoice_scheme_dealer_share",
            "invoice_scheme_tml_share",
            "invoice_scheme_total_amount",
            "invoice_yono_name",
            "invoice_yono_campaign_code",
            "invoice_yono_dealer_share",
            "invoice_yono_tml_share",
            "invoice_yono_total_amount",
            "invoice_exchange_name",
            "invoice_exchange_campaign_code",
            "invoice_exchange_dealer_share",
            "invoice_exchange_tml_share",
            "invoice_exchange_total_amount",



        )


class BookingInvoiceUpdateFormTeamLead(forms.ModelForm):
    is_temp_address = forms.ChoiceField(choices=SELECTION_CHOICES,widget=forms.Select(attrs={"class": "form-control w-20"}),)
    is_scheme = forms.ChoiceField(choices=SELECTION_CHOICES,widget=forms.Select(attrs={"class": "form-control w-20"}),)
    is_yono_scheme = forms.ChoiceField(choices=SELECTION_CHOICES,widget=forms.Select(attrs={"class": "form-control w-20"}),)
    is_finance = forms.ChoiceField(choices=SELECTION_CHOICES_FINANCE,widget=forms.Select(attrs={"class": "form-control w-40"}),)


    state = forms.ModelChoiceField(queryset=State.objects.all(), label="State")
    district = forms.ModelChoiceField(queryset=District.objects.all(), label="District")
    # temp address
    temp_state = forms.ModelChoiceField(queryset=State.objects.all(), label="State", required=False)
    temp_district = forms.ModelChoiceField(queryset=District.objects.all(), label="District", required=False)

    invoice_no = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))

    class Meta:
        model = BookingInvoice
        fields = (
            "invoice_no",
            "dse",
            "customer_salutation",
            "customer_name",
            "mobile",
            "email",
            "guardian_salutation",
            "guardian_name",
            "dob",
            "house_name",
            "place",
            "panchayath",
            "village",
            "post",
            "pin",
            "state",
            "district",
            "temp_house_name",
            "temp_place",
            "temp_panchayath",
            "temp_village",
            "temp_post",
            "temp_pin",
            "temp_state",
            "temp_district",
            # registration
            "reg_type",
            "rto",
            "reg_remarks",
            "any_tax_exemption",
            "tax_remarks",
            # insurance
            "insurance_type",
            "ncb_eligibility",
            "ncb_percentage",
            "any_other_discount",
            "insurance_remarks",
            "nominee_name",
            "dob_of_nominee",
            "nominee_relation",
            # scheme
            "scheme",
            "scheme_name",
            "institution_name",
            "amount",
            "yono_scheme_amount",
            # finance
            "finance",
            "branch",
            "loan_amount",
            "executive",

            "is_temp_address",
            "is_scheme",
            "is_yono_scheme",
            "is_finance",
        )
